/** @odoo-module **/
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { AddButtonListController } from './add_button_list_controller';

export const crmLeadListView = {
    ...listView,
    Controller: AddButtonListController,
    buttonTemplate: 'custom_crm.ListView.Buttons'
};

registry.category("views").add("crm_lead_list", crmLeadListView);
