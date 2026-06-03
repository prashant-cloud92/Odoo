/** @odoo-module **/

import { registry } from "@web/core/registry";
import { BookDashboard } from "./book_dashboard";

registry.category("actions").add(
    "library_dashboard",
    BookDashboard
);