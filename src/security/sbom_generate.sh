#!/bin/bash
# Generate Software Bill of Materials (SBOM) using Syft

set -e

echo "================================"
echo "SBOM Generation"
echo "================================"

# Configuration
TARGET="${1:-.}"
OUTPUT_FORMAT="${2:-spdx-json}"
REPORT_DIR="reports/security"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create report directory
mkdir -p "${REPORT_DIR}"

echo "Target: ${TARGET}"
echo "Output format: ${OUTPUT_FORMAT}"
echo ""

# Check if Syft is installed
if ! command -v syft &> /dev/null; then
    echo "Syft is not installed. Installing..."
    
    # Install Syft
    curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
    
    if [ $? -ne 0 ]; then
        echo "Failed to install Syft. Please install manually."
        exit 1
    fi
fi

echo "Syft version:"
syft version
echo ""

# Generate SBOM for current directory (Python packages)
echo "Generating SBOM for Python dependencies..."
syft packages dir:. \
    --output "${OUTPUT_FORMAT}=sbom-python-${TIMESTAMP}.json" \
    --file "${REPORT_DIR}/sbom-python-${TIMESTAMP}.json"

echo "Python SBOM generated: ${REPORT_DIR}/sbom-python-${TIMESTAMP}.json"

# Also generate in CycloneDX format
echo ""
echo "Generating SBOM in CycloneDX format..."
syft packages dir:. \
    --output "cyclonedx-json=sbom-cyclonedx-${TIMESTAMP}.json" \
    --file "${REPORT_DIR}/sbom-cyclonedx-${TIMESTAMP}.json"

echo "CycloneDX SBOM generated: ${REPORT_DIR}/sbom-cyclonedx-${TIMESTAMP}.json"

# Generate human-readable report
echo ""
echo "Generating human-readable SBOM..."
syft packages dir:. \
    --output "table" \
    --file "${REPORT_DIR}/sbom-table-${TIMESTAMP}.txt"

echo "Table SBOM generated: ${REPORT_DIR}/sbom-table-${TIMESTAMP}.txt"

# If Docker image provided, generate SBOM for it
IMAGE_NAME="${3}"
if [ ! -z "${IMAGE_NAME}" ]; then
    echo ""
    echo "Generating SBOM for Docker image: ${IMAGE_NAME}"
    
    syft packages "${IMAGE_NAME}" \
        --output "${OUTPUT_FORMAT}=sbom-docker-${TIMESTAMP}.json" \
        --file "${REPORT_DIR}/sbom-docker-${TIMESTAMP}.json"
    
    echo "Docker SBOM generated: ${REPORT_DIR}/sbom-docker-${TIMESTAMP}.json"
fi

echo ""
echo "================================"
echo "SBOM generation completed!"
echo "Reports saved to: ${REPORT_DIR}/"
echo "================================"

# List generated files
echo ""
echo "Generated SBOM files:"
ls -lh "${REPORT_DIR}"/sbom-*-${TIMESTAMP}.*

exit 0
