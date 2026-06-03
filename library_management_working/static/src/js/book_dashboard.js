/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class BookDashboard extends Component {

    setup() {
        this.orm = useService("orm");

        this.state = useState({
            total_books: 0,

            available_books: 0,
        });

        onWillStart(async () => {
            const result = await this.orm.call(
                "book.detail",
                "get_dashboard_data",
                []
            );

            this.state.total_books = result.total_books;

            this.state.available_books = result.available_books;
        });
    }
}

BookDashboard.template = "library_management_working.BookDashboard";