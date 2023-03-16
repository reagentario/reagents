@auth.requires_login()
def report1():
    response.title = "Posizione: "

    # si accede come https://web2py.anandamide.info/labinventory/report/report1.pdf/P
    # per generare il pdf

    sub_location = request.args[0]
    sub_location_exp = db((db.sublocations.sub_location_short==sub_location)).select(db.sublocations.sub_location)[0].sub_location
    rows = db((db.inventory.sub_location==sub_location)).select(orderby=db.inventory.item)

    fields = ['item']

    table = TABLE(THEAD(TR(TH(T("Name"), _width="90%", _align="left"), TH(T("Number"), _width="10%"))),
                  TBODY(*[TR(*[TD(row[field], _border="3") for field in fields]) \
                        for row in rows]), _border="1", _align="center", _width="90%")

    title = 'Laboratory Report'

    if request.extension == "pdf":
        from gluon.contrib.pyfpdf import FPDF, HTMLMixin

        # create a custom class with the required functionality
        class MyFPDF(FPDF, HTMLMixin):
            def header(self):
                "hook to draw custom page header (logo and title)"
                import os
                logo = os.path.join(request.env.web2py_path, "gluon", "contrib", "plus.png")
                self.image(logo, 10, 8, 23)
                self.set_font('Arial', 'B', 15)
                self.cell(65) # padding
                self.cell(60, 10, response.title+sub_location_exp+' ('+sub_location+')', 2, 1, 0, 'C')
                self.ln(20)

            def footer(self):
                "hook to draw custom page footer (printing page numbers)"
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
                self.cell(0, 10, txt, 0, 0, 'C')

        pdf = MyFPDF()
        # create a page and serialize/render HTML objects
        pdf.add_page()
        pdf.write_html(str(XML(table, sanitize=False)))
        # prepare PDF to download
        response.headers['Content-Type'] = 'application/pdf'
        return pdf.output(dest='S')
    else:
        # normal html view:
        return dict(title=title, table=table)


# in alternativa dopo add_page() puoi usare:

# data = [['First Name', 'Last Name', 'email', 'zip'],
#            ['Mike', 'Driscoll', 'mike@somewhere.com', '55555'],
#            ['John', 'Doe', 'jdoe@doe.com', '12345'],]

#    col_width = pdf.w / 4.5
#    row_height = pdf.font_size
#    for row in data:
#        for item in row:
#            pdf.cell(col_width, row_height*spacing,
#                     txt=item, border=1)
#        pdf.ln(row_height*spacing)
# cosi' hai maggior controllo sulle singole celle (e puoi definire il border)
