#!/usr/bin/env bash
# Create a new feature branch and directory structure

set -euo pipefail

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "${SCRIPT_DIR}/common.sh"

usage() {
    cat << EOF
Usage: $(basename "$0") FEATURE_NAME

Create a new feature branch and directory structure for SpecOps.

Arguments:
    FEATURE_NAME    Name of the feature (e.g., sso-deployment, monitoring-stack)

Examples:
    $(basename "$0") sso-deployment
    $(basename "$0") monitoring-stack

This will:
    1. Get the next available feature ID (e.g., 001, 002)
    2. Create a git branch: NNN-FEATURE_NAME
    3. Create feature directory: .specops/specs/NNN-FEATURE_NAME/
    4. Switch to the new branch
EOF
}

main() {
    # Check arguments
    if [[ $# -ne 1 ]]; then
        usage
        exit 1
    fi
    
    local feature_name="$1"
    
    # Validate feature name (alphanumeric and hyphens only)
    if ! [[ "${feature_name}" =~ ^[a-z0-9-]+$ ]]; then
        log_error "Feature name must contain only lowercase letters, numbers, and hyphens"
        exit 1
    fi
    
    # Check if we're in a git repository
    check_git_repo || exit 1
    
    # Check if .specops directory exists
    check_specops_dir || exit 1
    
    # Get next feature ID
    log_info "Determining next feature ID..."
    local feature_id
    feature_id=$(get_next_feature_id)
    
    local full_feature_name="${feature_id}-${feature_name}"
    log_info "Feature ID: ${full_feature_name}"
    
    # Check if branch already exists
    if git show-ref --verify --quiet "refs/heads/${full_feature_name}"; then
        log_error "Branch '${full_feature_name}' already exists"
        exit 1
    fi
    
    # Create feature directory
    log_info "Creating feature directory..."
    create_feature_dir "${full_feature_name}"
    
    # Create git branch
    log_info "Creating git branch: ${full_feature_name}"
    git checkout -b "${full_feature_name}"
    
    log_success "Feature created successfully!"
    log_info ""
    log_info "Next steps:"
    log_info "  1. Run /specops.specify to define infrastructure requirements"
    log_info "  2. Run /specops.plan to create technical implementation plan"
    log_info "  3. Run /specops.tasks to generate task breakdown"
    log_info "  4. Run /specops.implement to execute deployment"
    log_info ""
    log_info "Feature directory: .specops/specs/${full_feature_name}/"
}

main "$@"