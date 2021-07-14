from jinja2 import Template
from datetime import date

global temp

def gen_bill(my_list,disc,billno):
    try:
        temp = '''<!DOCTYPE html>
        <html>

        <head>
            <meta charset="utf-8" />
            <title>Invoice # : {{ billno }}</title>


    <style>
        .invoice-box {
            max-width: 350px;
            margin: 0;
            padding: 2px;
            border: 1px solid #eee;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
            font-size: 18px;
            line-height: 22px;
            font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
            color: #000000;
        }

        .invoice-box table {
            width: 100%;
            line-height: inherit;
            text-align: left;
        }

        .invoice-box table td {
            padding: 5px;
            vertical-align: top;
        }

        .invoice-box table tr td:nth-child(2) {
            text-align: right;
        }

        .invoice-box table tr.top table td {
            padding-bottom: 1px;
        }

        .invoice-box table tr.top table td.title {
            font-size: 45px;
            line-height: 45px;
            color: #333;
        }

        .invoice-box table tr.top table td.title1 {
            font-size: 12px;
            line-height: 12px;
            color: #808080;
            text-align: center;
        }

        .invoice-box table tr.information table td {
            padding-bottom: 10px;
        }

        .invoice-box table tr.heading td {
            background: #eee;
            border-bottom: 1px solid #ddd;
            font-weight: bold;
            padding-left: 30px;
            padding-right: 30px;

        }

        .invoice-box table tr.heading td:nth-child(2) {
            text-align: right;
        }

        .invoice-box table tr.details td {
            padding-bottom: 20px;
        }

        .invoice-box table tr.item td {
            border-bottom: 1px solid #eee;
            padding-left: 30px;
            padding-right: 30px;
        }

        .invoice-box table tr.item td:nth-child(2) {
            border-bottom: 1px solid #eee;
            text-align: right;
            padding-left: 30px;
            padding-right: 30px;
        }

        .invoice-box table tr.item.last td {
            border-bottom: none;
        }

        .invoice-box table tr.total td:nth-child(2) {
            border-top: 2px solid #eee;
            font-weight: bold;
            text-align: right;
            padding-left: 30px;
            padding-right: 30px;
        }

        .invoice-box table tr.totalcenter td {
            border-top: 2px solid #eee;
            text-align: center;
        }

        @media only screen and (max-width: 600px) {
            .invoice-box table tr.top table td {
                width: 100%;
                display: block;
                text-align: center;
            }

            .invoice-box table tr.information table td {
                width: 100%;
                display: block;
                text-align: center;
            }
        }

        .bottom {
            text-align: right;
        }

        /** RTL **/
        .invoice-box.rtl {
            direction: rtl;
            font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
        }

        .invoice-box.rtl table {
            text-align: right;
        }

        .invoice-box.rtl table tr td:nth-child(2) {
            text-align: right;
        }
    </style>
        </head>

        <body>
            <div class="invoice-box">
                <table cellpadding="0" cellspacing="0">
                    <tr class="top">
                        <td colspan="2">
                            <table>
                                <tr>
                                    <td class='title1'>
                                        Bill Of Supply - Dealer Under Composite Scheme
                                    </td>
                                </tr>
                            </table>
                            <table>
                                <tr>
                                    <td class="title">
                                        <img src="https://drive.google.com/uc?export=view&id=19G6sC_Dt6xvp9q8JCLVKBSNYR0LU5i1a"
                                            style="width: 100%; max-width: 350px" />
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <tr class="information">
                        <td colspan="2">
                            <table>
                                <tr>
                                    <td>
                                        Contact : 9819781011<br />
                                        GST #: 27AFIPJ1764M1Z2<br />
                                    </td>
                                    <td>
                                        Bill #: {{ billno }}<br />
                                        Date: {{ date_now }}
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <tr class="heading">
                        <td>Item</td>

                        <td>Price</td>
                    </tr>

                    {% for x in my_list %}

                    <tr class="item">
                        <td>{{ x[0] }}</td>

                        <td>&#2352 {{ x[1] }}</td>
                    </tr>

                    {% endfor %}
                </table>
                <table>
                    <tr class="total">
                        <td></td>

                        <td>Total: &#2352 {{ sum_items }}</td>
                    </tr>

                    <tr class="total">
                        <td></td>

                        <td> &#2352 {{ disc_sum_items }}</td>
                    </tr>

                </table>

                        <table>
            <tr class="totalcenter">
                <td>Thank You For Shopping With Us!!</td>
            </tr>

        </table>
            </div>
        </body>

        </html>
        '''
        sum_items = 0
        for i in my_list:
            sum_items+=int(i[1])
        date_now = date.today().strftime("%d/%m/%Y")
        t = Template(temp)
        if int(disc)==0:
            disc_sum = sum_items
        else:
            disc_sum = round((sum_items - sum_items*int(disc)/100)/10)*10
        billstr = t.render(billno=billno,date_now=date_now,my_list=my_list,sum_items=sum_items,disc_sum_items=disc_sum)
        with open('bills//'+str(billno)+'.html','w') as f:
            f.write(billstr)
        return sum_items
    except:
        return False