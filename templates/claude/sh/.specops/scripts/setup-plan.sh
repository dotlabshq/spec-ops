#!/usr/bin/env bash
# Set up planning artifacts for the current feature

set -euo pipefail

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "${SCRIPT_DIR}/common.sh"

usage() {
    cat << EOF
Usage: $(basename "$0")

Set up planning artifacts for the current feature.

This script:
    1. Validates that specification exists
    2. Creates plan.md from template
    3. Prepares for technical planning

Run this after completing the specification and before running /specops.plan

Environment Variables:
    SPECOPS_FEATURE    Override feature detection (e.g., "001-sso-deployment")
EOF
}

main() {
    # Check if we're in a git repository
    check_git_repo || exit 1
    
    # Check if .specops directory exists
    check_specops_dir || exit 1
    
    # Ensure constitution exists
    ensure_constitution || exit 1
    
    # Get current feature
    log_info "Detecting current feature..."
    local feature_id
    feature_id=$(get_current_feature) || exit 1
    log_info "Working on feature: ${feature_id}"
    
    # Ensure specification exists
    ensure_specification || exit 1
    
    local specops_dir
    specops_dir=$(get_specops_dir)
    local feature_dir="${specops_dir}/specs/${feature_id}"
    local plan_file="${feature_dir}/plan.md"
    
    # Check if plan already exists
    if [[ -f "${plan_file}" ]]; then
        log_warning "Plan already exists: ${plan_file}"
        log_info "To recreate, delete the file and run this script again"
        exit 0
    fi
    
    # Find template directory (go up from .specops to find templates)
    local git_root
    git_root=$(get_git_root)
    local template_file="${git_root}/.specops/templates/plan-template.md"
    
    # If template doesn't exist in project, try to copy from base
    if [[ ! -f "${template_file}" ]]; then
        log_warning "Template not found in project, using base template"
        # In actual usage, this would be in the installed package
        # For now, we assume it's been copied during project initialization
        log_error "Plan template not found. Please ensure project was initialized correctly."
        exit 1
    fi
    
    # Create plan from template
    log_info "Creating plan.md from template..."
    create_from_template "${template_file}" "${plan_file}"
    
    log_success "Plan setup complete!"
    log_info ""
    log_info "Next steps:"
    log_info "  1. Review the specification: ${feature_dir}/spec.md"
    log_info "  2. Run /specops.plan to create technical implementation plan"
    log_info "  3. Specify your technology choices and architecture"
    log_info ""
    log_info "Plan file: ${plan_file}"
}

# Handle --help flag
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    usage
    exit 0
fi

main "$@"