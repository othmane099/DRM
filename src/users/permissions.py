from typing import Final

CAN_CREATE_USER: Final[str] = "create_user"
CAN_CREATE_CATEGORY: Final[str] = "create_category"
CAN_CREATE_SUB_CATEGORY: Final[str] = "create_sub_category"
CAN_CREATE_TAG: Final[str] = "create_tag"
CAN_CREATE_DOCUMENT: Final[str] = "create_document"
CAN_CREATE_MY_DOCUMENT: Final[str] = "create_my_document"
CAN_MANAGE_DOCUMENT_HISTORY: Final[str] = "manage_document_history"
CAN_MANAGE_VERSION: Final[str] = "manage_version"
CAN_CREATE_VERSION: Final[str] = "create_version"

PERMISSIONS: Final[list[dict[str, str]]] = [
    {"name": "manage_user", "label": "Manage user"},
    {"name": CAN_CREATE_USER, "label": "Create user"},
    {"name": "edit_user", "label": "Edit user"},
    {"name": "delete_user", "label": "Delete user"},
    {"name": "manage_document", "label": "Manage document"},
    {"name": CAN_CREATE_DOCUMENT, "label": "Create document"},
    {"name": "edit_document", "label": "Edit document"},
    {"name": "delete_document", "label": "Delete document"},
    {"name": "show_document", "label": "Show document"},
    {"name": "manage_my_document", "label": "Manage my document"},
    {"name": "edit_my_document", "label": "Edit my document"},
    {"name": "delete_my_document", "label": "Delete my document"},
    {"name": "show_my_document", "label": "Show my document"},
    {"name": CAN_CREATE_MY_DOCUMENT, "label": "Create my document"},
    {"name": CAN_MANAGE_DOCUMENT_HISTORY, "label": "Manage document history"},
    {"name": "download_document", "label": "Download document"},
    {"name": "preview_document", "label": "Preview document"},
    {"name": "manage_share_document", "label": "Manage share document"},
    {"name": "delete_share_document", "label": "Delete share document"},
    {"name": "create_share_document", "label": "Create share document"},
    {"name": "manage_reminder", "label": "Manage reminder"},
    {"name": "create_reminder", "label": "Create reminder"},
    {"name": "edit_reminder", "label": "Edit reminder"},
    {"name": "delete_reminder", "label": "Delete reminder"},
    {"name": "show_reminder", "label": "Show reminder"},
    {"name": "manage_my_reminder", "label": "Manage my reminder"},
    {"name": "manage_comment", "label": "Manage comment"},
    {"name": "create_comment", "label": "Create comment"},
    {"name": CAN_MANAGE_VERSION, "label": "Manage version"},
    {"name": CAN_CREATE_VERSION, "label": "Create version"},
    {"name": "manage_email_settings", "label": "Manage email settings"},
    {"name": "manage_mail", "label": "Manage mail"},
    {"name": "send_mail", "label": "Send mail"},
    {"name": "manage_category", "label": "Manage category"},
    {"name": CAN_CREATE_CATEGORY, "label": "Create category"},
    {"name": "edit_category", "label": "Edit category"},
    {"name": "delete_category", "label": "Delete category"},
    {"name": "manage_sub_category", "label": "Manage sub category"},
    {"name": CAN_CREATE_SUB_CATEGORY, "label": "Create sub category"},
    {"name": "edit_sub_category", "label": "Edit sub category"},
    {"name": "delete_sub_category", "label": "Delete sub category"},
    {"name": "manage_tag", "label": "Manage tag"},
    {"name": CAN_CREATE_TAG, "label": "Create tag"},
    {"name": "edit_tag", "label": "Edit tag"},
    {"name": "delete_tag", "label": "Delete tag"},
    {"name": "manage_contact", "label": "Manage contact"},
    {"name": "create_contact", "label": "Create contact"},
    {"name": "edit_contact", "label": "Edit contact"},
    {"name": "delete_contact", "label": "Delete contact"},
    {"name": "manage_note", "label": "Manage note"},
    {"name": "create_note", "label": "Create note"},
    {"name": "edit_note", "label": "Edit note"},
    {"name": "delete_note", "label": "Delete note"},
    {"name": "manage_logged_history", "label": "Manage logged history"},
    {"name": "delete_logged_history", "label": "Delete logged history"},
    {"name": "manage_pricing_transaction", "label": "Manage pricing transaction"},
    {"name": "manage_account_settings", "label": "Manage account settings"},
    {"name": "manage_password_settings", "label": "Manage password settings"},
    {"name": "manage_general_settings", "label": "Manage general settings"},
    {"name": "manage_company_settings", "label": "Manage company settings"},
]
