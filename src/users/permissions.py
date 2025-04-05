from typing import Final

# User
CAN_CREATE_USER: Final[str] = "create_user"
CAN_EDIT_USER: Final[str] = "edit_user"
CAN_DELETE_USER: Final[str] = "delete_user"
CAN_MANAGE_USER: Final[str] = "manage_user"

# Document
CAN_MANAGE_DOCUMENT: Final[str] = "manage_document"
CAN_CREATE_DOCUMENT: Final[str] = "create_document"
CAN_EDIT_DOCUMENT: Final[str] = "edit_document"
CAN_DELETE_DOCUMENT: Final[str] = "delete_document"
CAN_SHOW_DOCUMENT: Final[str] = "show_document"
CAN_MANAGE_MY_DOCUMENT: Final[str] = "manage_my_document"
CAN_CREATE_MY_DOCUMENT: Final[str] = "create_my_document"
CAN_EDIT_MY_DOCUMENT: Final[str] = "edit_my_document"
CAN_DELETE_MY_DOCUMENT: Final[str] = "delete_my_document"
CAN_SHOW_MY_DOCUMENT: Final[str] = "show_my_document"
CAN_MANAGE_DOCUMENT_HISTORY: Final[str] = "manage_document_history"
CAN_DOWNLOAD_DOCUMENT: Final[str] = "download_document"
CAN_PREVIEW_DOCUMENT: Final[str] = "preview_document"

# Share Document
CAN_MANAGE_SHARE_DOCUMENT: Final[str] = "manage_share_document"
CAN_DELETE_SHARE_DOCUMENT: Final[str] = "delete_share_document"
CAN_CREATE_SHARE_DOCUMENT: Final[str] = "create_share_document"

# Reminder
CAN_MANAGE_REMINDER: Final[str] = "manage_reminder"
CAN_CREATE_REMINDER: Final[str] = "create_reminder"
CAN_EDIT_REMINDER: Final[str] = "edit_reminder"
CAN_DELETE_REMINDER: Final[str] = "delete_reminder"
CAN_SHOW_REMINDER: Final[str] = "show_reminder"
CAN_MANAGE_MY_REMINDER: Final[str] = "manage_my_reminder"

# Comment
CAN_MANAGE_COMMENT: Final[str] = "manage_comment"
CAN_CREATE_COMMENT: Final[str] = "create_comment"

# Version
CAN_MANAGE_VERSION: Final[str] = "manage_version"
CAN_CREATE_VERSION: Final[str] = "create_version"

# Email & Mail
CAN_MANAGE_EMAIL_SETTINGS: Final[str] = "manage_email_settings"
CAN_MANAGE_MAIL: Final[str] = "manage_mail"
CAN_SEND_MAIL: Final[str] = "send_mail"

# Category & Sub-category
CAN_MANAGE_CATEGORY: Final[str] = "manage_category"
CAN_CREATE_CATEGORY: Final[str] = "create_category"
CAN_EDIT_CATEGORY: Final[str] = "edit_category"
CAN_DELETE_CATEGORY: Final[str] = "delete_category"
CAN_MANAGE_SUB_CATEGORY: Final[str] = "manage_sub_category"
CAN_CREATE_SUB_CATEGORY: Final[str] = "create_sub_category"
CAN_EDIT_SUB_CATEGORY: Final[str] = "edit_sub_category"
CAN_DELETE_SUB_CATEGORY: Final[str] = "delete_sub_category"

# Tag
CAN_MANAGE_TAG: Final[str] = "manage_tag"
CAN_CREATE_TAG: Final[str] = "create_tag"
CAN_EDIT_TAG: Final[str] = "edit_tag"
CAN_DELETE_TAG: Final[str] = "delete_tag"

# Contact
CAN_MANAGE_CONTACT: Final[str] = "manage_contact"
CAN_CREATE_CONTACT: Final[str] = "create_contact"
CAN_EDIT_CONTACT: Final[str] = "edit_contact"
CAN_DELETE_CONTACT: Final[str] = "delete_contact"

# Note
CAN_MANAGE_NOTE: Final[str] = "manage_note"
CAN_CREATE_NOTE: Final[str] = "create_note"
CAN_EDIT_NOTE: Final[str] = "edit_note"
CAN_DELETE_NOTE: Final[str] = "delete_note"

# Logged history
CAN_MANAGE_LOGGED_HISTORY: Final[str] = "manage_logged_history"
CAN_DELETE_LOGGED_HISTORY: Final[str] = "delete_logged_history"

# Settings
CAN_MANAGE_PRICING_TRANSACTION: Final[str] = "manage_pricing_transaction"
CAN_MANAGE_ACCOUNT_SETTINGS: Final[str] = "manage_account_settings"
CAN_MANAGE_PASSWORD_SETTINGS: Final[str] = "manage_password_settings"
CAN_MANAGE_GENERAL_SETTINGS: Final[str] = "manage_general_settings"
CAN_MANAGE_COMPANY_SETTINGS: Final[str] = "manage_company_settings"

PERMISSIONS: Final[list[dict[str, str]]] = [
    {"name": CAN_MANAGE_USER, "label": "Manage user"},
    {"name": CAN_CREATE_USER, "label": "Create user"},
    {"name": CAN_EDIT_USER, "label": "Edit user"},
    {"name": CAN_DELETE_USER, "label": "Delete user"},
    {"name": CAN_MANAGE_DOCUMENT, "label": "Manage document"},
    {"name": CAN_CREATE_DOCUMENT, "label": "Create document"},
    {"name": CAN_EDIT_DOCUMENT, "label": "Edit document"},
    {"name": CAN_DELETE_DOCUMENT, "label": "Delete document"},
    {"name": CAN_SHOW_DOCUMENT, "label": "Show document"},
    {"name": CAN_MANAGE_MY_DOCUMENT, "label": "Manage my document"},
    {"name": CAN_CREATE_MY_DOCUMENT, "label": "Create my document"},
    {"name": CAN_EDIT_MY_DOCUMENT, "label": "Edit my document"},
    {"name": CAN_DELETE_MY_DOCUMENT, "label": "Delete my document"},
    {"name": CAN_SHOW_MY_DOCUMENT, "label": "Show my document"},
    {"name": CAN_MANAGE_DOCUMENT_HISTORY, "label": "Manage document history"},
    {"name": CAN_DOWNLOAD_DOCUMENT, "label": "Download document"},
    {"name": CAN_PREVIEW_DOCUMENT, "label": "Preview document"},
    {"name": CAN_MANAGE_SHARE_DOCUMENT, "label": "Manage share document"},
    {"name": CAN_DELETE_SHARE_DOCUMENT, "label": "Delete share document"},
    {"name": CAN_CREATE_SHARE_DOCUMENT, "label": "Create share document"},
    {"name": CAN_MANAGE_REMINDER, "label": "Manage reminder"},
    {"name": CAN_CREATE_REMINDER, "label": "Create reminder"},
    {"name": CAN_EDIT_REMINDER, "label": "Edit reminder"},
    {"name": CAN_DELETE_REMINDER, "label": "Delete reminder"},
    {"name": CAN_SHOW_REMINDER, "label": "Show reminder"},
    {"name": CAN_MANAGE_MY_REMINDER, "label": "Manage my reminder"},
    {"name": CAN_MANAGE_COMMENT, "label": "Manage comment"},
    {"name": CAN_CREATE_COMMENT, "label": "Create comment"},
    {"name": CAN_MANAGE_VERSION, "label": "Manage version"},
    {"name": CAN_CREATE_VERSION, "label": "Create version"},
    {"name": CAN_MANAGE_EMAIL_SETTINGS, "label": "Manage email settings"},
    {"name": CAN_MANAGE_MAIL, "label": "Manage mail"},
    {"name": CAN_SEND_MAIL, "label": "Send mail"},
    {"name": CAN_MANAGE_CATEGORY, "label": "Manage category"},
    {"name": CAN_CREATE_CATEGORY, "label": "Create category"},
    {"name": CAN_EDIT_CATEGORY, "label": "Edit category"},
    {"name": CAN_DELETE_CATEGORY, "label": "Delete category"},
    {"name": CAN_MANAGE_SUB_CATEGORY, "label": "Manage sub category"},
    {"name": CAN_CREATE_SUB_CATEGORY, "label": "Create sub category"},
    {"name": CAN_EDIT_SUB_CATEGORY, "label": "Edit sub category"},
    {"name": CAN_DELETE_SUB_CATEGORY, "label": "Delete sub category"},
    {"name": CAN_MANAGE_TAG, "label": "Manage tag"},
    {"name": CAN_CREATE_TAG, "label": "Create tag"},
    {"name": CAN_EDIT_TAG, "label": "Edit tag"},
    {"name": CAN_DELETE_TAG, "label": "Delete tag"},
    {"name": CAN_MANAGE_CONTACT, "label": "Manage contact"},
    {"name": CAN_CREATE_CONTACT, "label": "Create contact"},
    {"name": CAN_EDIT_CONTACT, "label": "Edit contact"},
    {"name": CAN_DELETE_CONTACT, "label": "Delete contact"},
    {"name": CAN_MANAGE_NOTE, "label": "Manage note"},
    {"name": CAN_CREATE_NOTE, "label": "Create note"},
    {"name": CAN_EDIT_NOTE, "label": "Edit note"},
    {"name": CAN_DELETE_NOTE, "label": "Delete note"},
    {"name": CAN_MANAGE_LOGGED_HISTORY, "label": "Manage logged history"},
    {"name": CAN_DELETE_LOGGED_HISTORY, "label": "Delete logged history"},
    {"name": CAN_MANAGE_PRICING_TRANSACTION, "label": "Manage pricing transaction"},
    {"name": CAN_MANAGE_ACCOUNT_SETTINGS, "label": "Manage account settings"},
    {"name": CAN_MANAGE_PASSWORD_SETTINGS, "label": "Manage password settings"},
    {"name": CAN_MANAGE_GENERAL_SETTINGS, "label": "Manage general settings"},
    {"name": CAN_MANAGE_COMPANY_SETTINGS, "label": "Manage company settings"},
]
