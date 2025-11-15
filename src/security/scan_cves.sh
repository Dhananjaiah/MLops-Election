#!/bin/bash
# Scan for CVEs in Docker images using Trivy

set -e

echo "================================"
echo "Docker Image Security Scan"
echo "================================"

# Configuration
IMAGE_NAME="${1:-election-prediction-api}"
IMAGE_TAG="${2:-latest}"
FULL_IMAGE="${IMAGE_NAME}:${IMAGE_TAG}"
SEVERITY="${3:-HIGH,CRITICAL}"
OUTPUT_FORMAT="${4:-table}"
REPORT_DIR="reports/security"

# Create report directory
mkdir -p "${REPORT_DIR}"

echo "Scanning image: ${FULL_IMAGE}"
echo "Severity levels: ${SEVERITY}"
echo ""

# Check if Trivy is installed
if ! command -v trivy &> /dev/null; then
    echo "Trivy is not installed. Installing..."
    
    # Install Trivy based on OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
        echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
        sudo apt-get update
        sudo apt-get install trivy -y
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install trivy
    else
        echo "Unsupported OS. Please install Trivy manually."
        exit 1
    fi
fi

echo "Trivy version:"
trivy --version
echo ""

# Update vulnerability database
echo "Updating vulnerability database..."
trivy image --download-db-only
echo ""

# Scan Docker image
echo "Scanning Docker image..."
trivy image \
    --severity "${SEVERITY}" \
    --format "${OUTPUT_FORMAT}" \
    --output "${REPORT_DIR}/trivy-report-${IMAGE_TAG}.txt" \
    "${FULL_IMAGE}"

# Also generate JSON report for automation
trivy image \
    --severity "${SEVERITY}" \
    --format json \
    --output "${REPORT_DIR}/trivy-report-${IMAGE_TAG}.json" \
    "${FULL_IMAGE}"

echo ""
echo "Scan completed!"
echo "Reports saved to ${REPORT_DIR}/"
echo ""

# Check if vulnerabilities found
VULN_COUNT=$(trivy image --severity "${SEVERITY}" --format json "${FULL_IMAGE}" 2>/dev/null | jq '[.Results[].Vulnerabilities // []] | add | length')

if [ "${VULN_COUNT}" -gt 0 ]; then
    echo "⚠️  WARNING: ${VULN_COUNT} vulnerabilities found!"
    echo "Review the report at: ${REPORT_DIR}/trivy-report-${IMAGE_TAG}.txt"
    exit 1
else
    echo "✓ No vulnerabilities found!"
    exit 0
fi
