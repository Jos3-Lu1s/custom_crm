/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";

export class AddButtonListController extends ListController {
  setup() {
    super.setup();
  }

  leadsOptions() {
    this.actionService.doAction({
      type: "ir.actions.act_window",
      name: "Reintentar oportunidades perdidas",
      res_model: "crm.lead.wizard",
      view_mode: "form",
      view_type: "form",
      target: "new",
      views: [[false, "form"]],
      res_id: false,
    });
  }
}
