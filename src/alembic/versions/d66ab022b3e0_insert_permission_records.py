"""insert permission records

Revision ID: d66ab022b3e0
Revises: e1aa463b4510
Create Date: 2025-03-22 15:54:08.912443

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import column, table

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d66ab022b3e0"
down_revision: Union[str, None] = "e1aa463b4510"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create a table representation for the existing permissions table
    permissions_table = table(
        "permissions",
        column("id", sa.Integer),
        column("name", sa.String),
        column("label", sa.String),
        # BaseEntity fields, assuming your BaseEntity contains these
        column("created_at", sa.DateTime),
        column("updated_at", sa.DateTime),
    )

    # Insert the permissions data
    op.bulk_insert(
        permissions_table,
        [
            {"name": "manage_user", "label": "Manage user"},
            {"name": "create_user", "label": "Create user"},
            {"name": "edit_user", "label": "Edit user"},
            {"name": "delete_user", "label": "Delete user"},
            {"name": "manage_document", "label": "Manage document"},
            {"name": "create_document", "label": "Create document"},
            {"name": "edit_document", "label": "Edit document"},
            {"name": "delete_document", "label": "Delete document"},
            {"name": "show_document", "label": "Show document"},
            {"name": "manage_my_document", "label": "Manage my document"},
            {"name": "edit_my_document", "label": "Edit my document"},
            {"name": "delete_my_document", "label": "Delete my document"},
            {"name": "show_my_document", "label": "Show my document"},
            {"name": "create_my_document", "label": "Create my document"},
            {"name": "manage_document_history", "label": "Manage document history"},
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
            {"name": "manage_version", "label": "Manage version"},
            {"name": "create_version", "label": "Create version"},
            {"name": "manage_email_settings", "label": "Manage email settings"},
            {"name": "manage_mail", "label": "Manage mail"},
            {"name": "send_mail", "label": "Send mail"},
            {"name": "manage_category", "label": "Manage category"},
            {"name": "create_category", "label": "Create category"},
            {"name": "edit_category", "label": "Edit category"},
            {"name": "delete_category", "label": "Delete category"},
            {"name": "manage_sub_category", "label": "Manage sub category"},
            {"name": "create_sub_category", "label": "Create sub category"},
            {"name": "edit_sub_category", "label": "Edit sub category"},
            {"name": "delete_sub_category", "label": "Delete sub category"},
            {"name": "manage_tag", "label": "Manage tag"},
            {"name": "create_tag", "label": "Create tag"},
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
            {
                "name": "manage_pricing_transaction",
                "label": "Manage pricing transaction",
            },
            {"name": "manage_account_settings", "label": "Manage account settings"},
            {"name": "manage_password_settings", "label": "Manage password settings"},
            {"name": "manage_general_settings", "label": "Manage general settings"},
            {"name": "manage_company_settings", "label": "Manage company settings"},
        ],
    )


def downgrade():
    # Delete all the permissions added in this migration
    op.execute(
        """
        DELETE FROM permissions 
        WHERE name IN (
            'manage_user', 'create_user', 'edit_user', 'delete_user',
            'manage_document', 'create_document', 'edit_document', 'delete_document', 'show_document',
            'manage_my_document', 'edit_my_document', 'delete_my_document', 'show_my_document', 'create_my_document',
            'manage_document_history', 'download_document', 'preview_document',
            'manage_share_document', 'delete_share_document', 'create_share_document',
            'manage_reminder', 'create_reminder', 'edit_reminder', 'delete_reminder', 'show_reminder', 'manage_my_reminder',
            'manage_comment', 'create_comment',
            'manage_version', 'create_version',
            'manage_email_settings', 'manage_mail', 'send_mail',
            'manage_category', 'create_category', 'edit_category', 'delete_category',
            'manage_sub_category', 'create_sub_category', 'edit_sub_category', 'delete_sub_category',
            'manage_tag', 'create_tag', 'edit_tag', 'delete_tag',
            'manage_contact', 'create_contact', 'edit_contact', 'delete_contact',
            'manage_note', 'create_note', 'edit_note', 'delete_note',
            'manage_logged_history', 'delete_logged_history',
            'manage_pricing_transaction',
            'manage_account_settings', 'manage_password_settings', 'manage_general_settings', 'manage_company_settings'
        )
    """
    )
