/** @odoo-module **/
import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { AddButtonKanbanController } from './add_button_kanban_controller';

export const crmLeadKanbanView = {
    ...kanbanView,
    Controller: AddButtonKanbanController,
    buttonTemplate: 'custom_crm.KanbanView.Buttons'
};

registry.category("views").add("crm_lead_kanban", crmLeadKanbanView);
