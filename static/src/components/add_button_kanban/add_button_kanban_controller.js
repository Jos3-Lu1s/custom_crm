import { KanbanController } from "@web/views/kanban/kanban_controller";

export class AddButtonKanbanController extends KanbanController {
    setup() {
        super.setup();
    }

    leadsOptions(){
        this.actionService.doAction({
            type:'ir.actions.act_window',
            name:'lost leads',
            res_model: 'crm.lead.wizard',
            view_mode:'form',
            view_type:'form',
            target:'new',
            views:[[false, 'form']],
            res_id:false,
        })
    }
}
