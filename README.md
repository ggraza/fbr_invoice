## Fbr Invoice

Fbr Invoice Return, Integrate You ERPNext POS-App with Pakistan FBR

## Installation

To install the FBR_Invoice custom app, follow the steps below:

1. Make sure you have Frappe installed and set up in your environment.
2. Clone the FBR_Invoice repository from GitHub into the `apps` directory of your Frappe instance:

```
cd /path/to/frappe-bench
bench get-app fbr_invoice https://github.com/ggraza/fbr_invoice.git
```

3. Install the app using the Frappe Bench:

```
cd /path/to/frappe-bench
bench --site your-site-name install-app fbr_invoice
```

#### Print Formate

```
<style>
    .print-format table, .print-format tr, 
    .print-format td, .print-format div, .print-format p {
        line-height: 100%;
        vertical-align: middle;
    }
    @media screen {
        .print-format {
            width: 4in;
            padding: 0.15in;
            min-height: 8in;
        }
    }
    p.text-center {
        font-size: 11px; /* Adjust the font size as needed */
    }
    table.table-condensed th, table.table-condensed td {
        font-size: 10px; /* Adjust the font size as needed */
        margin: 0px 0px
    }
    thead {
        margin-top: 0; /* Adjust the margin as needed */
    }

    /* Add this style to change table border color to black */
    table {
        border: 1px solid black;
    }
    .table {
    margin: 5px 0px;
    margin-bottom: 0px;
    }

    /* Add this style to change table header (thead) border color to black */
    table thead th {
        border: 1px solid black;
    }

    /* Add this style to change table cell (td) border color to black */
    table td {
        border: 1px solid black;
    }
    /* Reduce row height for table rows */
    table.table-condensed tr {
        line-height: 80%; /* Adjust this value as needed to reduce the row height */
    }
    .table-condensed.no-border {
        margin-top: 0;
    }

</style>

{% if letter_head %}
    {{ letter_head }}
{% endif %}

<p class="text-center">

</p>
<p class="text-center" style="margin-bottom: 0rem">
    <b>{{ _("") }}</b> {{ doc.company }}<br>
    <b class="text-center">{{ doc.select_print_heading or _("Sale Invoice") }}</b><br>
    <b>{{ _("") }}</b> {{ doc.get_formatted("posting_date") }} {{ doc.get_formatted("posting_time") }}<br>
    <b>{{ _("") }}</b> {{ doc.name }}<br>
    <b>{{ _("Tax Information: LTO-Lahore") }}</b><br>
    <b>{{ _("PoS No") }}</b> {{ doc.pos_id }} - {{ _("NTN No") }} {{ doc.ntn_no }}
</p>
<table class="table table-condensed">
    <thead>
        <tr>
            <th width="45%">{{ _("Item") }}</th>
            <th width="15%" class="text-right">{{ _("Qty") }}</th>
            <th width="20%" class="text-right">{{ _("Rate") }}</th>
            <th width="20%" class="text-right">{{ _("Amount") }}</th>
        </tr>
    </thead>
    <tbody>
        {%- for item in doc.items -%}
        <tr>
            <td>{{ item.item_name }}</td>
            <td class="text-right">{{ item.qty }}</td>
            <td class="text-right">{{ item.get_formatted("rate") }}</td>
            <td class="text-right">{{ item.get_formatted("amount") }}</td>
        </tr>
        {%- endfor -%}
    </tbody>
</table>
<table class="table table-condensed no-border">
    <tbody>
        <tr>
            {% if doc.flags.show_inclusive_tax_in_print %}
                <td class="text-right" style="width: 70%">
                    {{ _("Total Excl. Tax") }}
                </td>
                <td class="text-right">
                    {{ doc.get_formatted("net_total", doc) }}
                </td>
            {% else %}
                <td class="text-right" style="width: 70%">
                    {{ _("Total") }}
                </td>
                <td class="text-right">
                    {{ doc.get_formatted("total", doc) }}
                </td>
            {% endif %}
        </tr>
        {%- for row in doc.taxes -%}
          {%- if not row.included_in_print_rate or doc.flags.show_inclusive_tax_in_print -%}
            <tr>
                <td class="text-right" style="width: 70%">
                    {% if '%' in row.description %}
                        {{ row.description }}
                    {% else %}
                        {{ row.description }}@{{ row.rate }}%
                    {% endif %}
                </td>
                <td class="text-right">
                    {{ row.get_formatted("tax_amount", doc) }}
                </td>
            <tr>
          {%- endif -%}
        {%- endfor -%}

        {%- if doc.discount_amount -%}
        <tr>
            <td class="text-right" style="width: 75%">
                {{ _("Discount") }}
            </td>
            <td class="text-right">
                {{ doc.get_formatted("discount_amount") }}
            </td>
        </tr>
        {%- endif -%}
        {%- if doc.rounded_total -%}
        <tr>
            <td class="text-right" style="width: 75%">
                <b>{{ _("Net Total") }}</b>
            </td>
            <td class="text-right">
                {{ doc.get_formatted("rounded_total") }}
            </td>
        </tr>
        {%- endif -%}
        {%- for row in doc.payments -%}
            <tr>
                <td class="text-right" style="width: 70%">
                    {{ row.mode_of_payment }}
                </td>
                <td class="text-right">
                    {{ row.get_formatted("amount", doc) }}
                </td>
            <tr>
        {%- endfor -%}
        <tr>
            <td class="text-right" style="width: 75%">
                <b>{{ _("Paid Amount") }}</b>
            </td>
            <td class="text-right">
                {{ doc.get_formatted("paid_amount") }}
            </td>
        </tr>
        {%- if doc.change_amount -%}
            <tr>
                <td class="text-right" style="width: 75%">
                    <b>{{ _("Change Amount") }}</b>
                </td>
                <td class="text-right">
                    {{ doc.get_formatted("change_amount") }}
                </td>
            </tr>
        {%- endif -%}
    </tbody>
</table>
<!-- Removed the <hr> tag here -->
<p>{{ doc.terms or "" }}</p>
<style>
    .columns {
        display: flex;
        justify-content: space-between;
    }
    .left-column {
        width: 55%; /* Adjust the width as needed */
        font-size: 11px; /* Adjust the font size as needed */
    }
    .right-column {
        width: 40%; /* Adjust the width as needed */
        font-size: 11px; /* Adjust the font size as needed */
    }
</style>

<div class="columns" style="font-size: 11px">
    <div class="text-left">
        <p>{{ _("The sale value includes GST where leviable") }}</p>
        <p>{{ doc.company }}{{ _(" Undertaking:I have checked goods & have no complaints in this regards") }}</p>
        <p><b>{{ _("No Refund & No Exchange") }}</b></p>
    </div>
    <div class="text-right" style="width: 75%">
        <img src="/assets/fbr_invoice/images/pos.png" style="max-width: 80px; max-height: 80px;">
    </div>
    <div class="text-right">
        {% set qr_code_url = "/files/qrcodes/" + doc.name + ".png" %}
        <img src="{{ qr_code_url }}" style="max-width: 90px; max-height: 90px;">
    </div>
</div>
<p class="text-center"><b>{{ _("FBR Invoice No.:") }}</b> {{ doc.fbr_invoice_no }}</p>
<p class="text-center"><b></b>Verify this invoice through FBR TaxAssan Mobile app or SMS at 9966 and win exciting prises in draw.</p>
<p class="text-center"><b>{{ _("For any Assistance, Please Contact Customer Care:") }}:</b> 0301-4435688</p>
<p class="text-center">{{ _("Thank you for visiting ") }}{{ doc.company }}{{ _(", We look forward to Welcome You again.") }}</p>
<p class="text-center">Online Ordering <b>{{ _("g2virtu.com") }}</b></p>
```

#### License

MIT

