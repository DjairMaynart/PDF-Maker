from pdfmaker import Document

# Document example

# Document initialization
d = Document()

# Definition of styles to be used
d.style_config(name='first_page_title', fontSize=80, fontName='Helvetica-Bold', alignment=1)
d.style_config(name='large_title', fontSize=20, fontName='Helvetica-Bold')
d.style_config(name='caption', fontSize=6, fontName='Helvetica-Bold', textColor=(1,0,0), alignment=1)
d.table_style(name='table2', backgroundColor=(0.9,0.9,0.9), textColor=(0,0,0.5), header=False)

# First page
d.add_space(100)
d.add_section(text='Example Document', style='first_page_title')
d.add_space(70)
d.add_image('Example.png', position='center', size_proportions=1.5)
d.new_page()

# Start page count and template images on every page
d.toggle_page_count()
d.add_template_image(name='watermark',file='Example.png', axisx='right', size_proportions=0.2, posx= 10, posy=20)

# Next pages
d.add_section('Title Example', style = 'large_title')
d.add_space()
# First section: Image example
d.add_title('Section 1')
d.add_space()
d.add_paragraph('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel feugiat mauris. Nullam tincidunt quam eget arcu mattis ornare. Sed porttitor leo ut nisi molestie, non lobortis purus pharetra. Phasellus dignissim libero odio, nec blandit nibh euismod nec. Nunc bibendum malesuada nisl sed bibendum. Etiam sit amet est nec mauris ultricies convallis sit amet sed nisl. Cras placerat in odio eu pretium. Sed accumsan ex dolor, sit amet porttitor sem faucibus et. Nullam mi velit, bibendum eget est rhoncus, ullamcorper vehicula massa. Donec mollis orci a turpis semper mollis. Cras mollis lectus non tellus mattis pharetra. Nunc lorem dolor, rutrum eget ultricies non, cursus eu diam.')
d.add_paragraph('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel feugiat mauris. Nullam tincidunt quam eget arcu mattis ornare. Sed porttitor leo ut nisi molestie, non lobortis purus pharetra. Phasellus dignissim libero odio, nec blandit nibh euismod nec. Nunc bibendum malesuada nisl sed bibendum. Etiam sit amet est nec mauris ultricies convallis sit amet sed nisl. Cras placerat in odio eu pretium. Sed accumsan ex dolor, sit amet porttitor sem faucibus et. Nullam mi velit, bibendum eget est rhoncus, ullamcorper vehicula massa. Donec mollis orci a turpis semper mollis. Cras mollis lectus non tellus mattis pharetra. Nunc lorem dolor, rutrum eget ultricies non, cursus eu diam.')
d.add_image('Example.png', position='center')
d.add_section('Example image', style='caption')
d.add_space()
d.add_paragraph('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel feugiat mauris. Nullam tincidunt quam eget arcu mattis ornare. Sed porttitor leo ut nisi molestie, non lobortis purus pharetra. Phasellus dignissim libero odio, nec blandit nibh euismod nec. Nunc bibendum malesuada nisl sed bibendum. Etiam sit amet est nec mauris ultricies convallis sit amet sed nisl. Cras placerat in odio eu pretium. Sed accumsan ex dolor, sit amet porttitor sem faucibus et. Nullam mi velit, bibendum eget est rhoncus, ullamcorper vehicula massa. Donec mollis orci a turpis semper mollis. Cras mollis lectus non tellus mattis pharetra. Nunc lorem dolor, rutrum eget ultricies non, cursus eu diam.')
d.add_paragraph('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel feugiat mauris. Nullam tincidunt quam eget arcu mattis ornare. Sed porttitor leo ut nisi molestie, non lobortis purus pharetra. Phasellus dignissim libero odio, nec blandit nibh euismod nec. Nunc bibendum malesuada nisl sed bibendum. Etiam sit amet est nec mauris ultricies convallis sit amet sed nisl. Cras placerat in odio eu pretium. Sed accumsan ex dolor, sit amet porttitor sem faucibus et. Nullam mi velit, bibendum eget est rhoncus, ullamcorper vehicula massa. Donec mollis orci a turpis semper mollis. Cras mollis lectus non tellus mattis pharetra. Nunc lorem dolor, rutrum eget ultricies non, cursus eu diam.')
d.add_paragraph('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel feugiat mauris. Nullam tincidunt quam eget arcu mattis ornare. Sed porttitor leo ut nisi molestie, non lobortis purus pharetra. Phasellus dignissim libero odio, nec blandit nibh euismod nec. Nunc bibendum malesuada nisl sed bibendum. Etiam sit amet est nec mauris ultricies convallis sit amet sed nisl. Cras placerat in odio eu pretium. Sed accumsan ex dolor, sit amet porttitor sem faucibus et. Nullam mi velit, bibendum eget est rhoncus, ullamcorper vehicula massa. Donec mollis orci a turpis semper mollis. Cras mollis lectus non tellus mattis pharetra. Nunc lorem dolor, rutrum eget ultricies non, cursus eu diam.')
d.add_paragraph('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel feugiat mauris. Nullam tincidunt quam eget arcu mattis ornare. Sed porttitor leo ut nisi molestie, non lobortis purus pharetra. Phasellus dignissim libero odio, nec blandit nibh euismod nec. Nunc bibendum malesuada nisl sed bibendum. Etiam sit amet est nec mauris ultricies convallis sit amet sed nisl. Cras placerat in odio eu pretium. Sed accumsan ex dolor, sit amet porttitor sem faucibus et. Nullam mi velit, bibendum eget est rhoncus, ullamcorper vehicula massa. Donec mollis orci a turpis semper mollis. Cras mollis lectus non tellus mattis pharetra. Nunc lorem dolor, rutrum eget ultricies non, cursus eu diam.')
d.add_space()
# Second section: Table example
d.add_title('Section 2')
d.add_space()
d.add_paragraph('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel feugiat mauris. Nullam tincidunt quam eget arcu mattis ornare. Sed porttitor leo ut nisi molestie, non lobortis purus pharetra. Phasellus dignissim libero odio, nec blandit nibh euismod nec. Nunc bibendum malesuada nisl sed bibendum. Etiam sit amet est nec mauris ultricies convallis sit amet sed nisl. Cras placerat in odio eu pretium. Sed accumsan ex dolor, sit amet porttitor sem faucibus et. Nullam mi velit, bibendum eget est rhoncus, ullamcorper vehicula massa. Donec mollis orci a turpis semper mollis. Cras mollis lectus non tellus mattis pharetra. Nunc lorem dolor, rutrum eget ultricies non, cursus eu diam.')
d.add_space(15)
table = [['Table Header 1', 'Table Header 2'],['Table Text 1', 'Table Text 2'],['Table Text 3', 'Table Text 4']]
d.add_table(table, col_widths=[100,100])
d.add_space(2)
d.add_section('Example table', style='caption')
d.add_space()
d.add_paragraph('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel feugiat mauris. Nullam tincidunt quam eget arcu mattis ornare. Sed porttitor leo ut nisi molestie, non lobortis purus pharetra. Phasellus dignissim libero odio, nec blandit nibh euismod nec. Nunc bibendum malesuada nisl sed bibendum. Etiam sit amet est nec mauris ultricies convallis sit amet sed nisl. Cras placerat in odio eu pretium. Sed accumsan ex dolor, sit amet porttitor sem faucibus et. Nullam mi velit, bibendum eget est rhoncus, ullamcorper vehicula massa. Donec mollis orci a turpis semper mollis. Cras mollis lectus non tellus mattis pharetra. Nunc lorem dolor, rutrum eget ultricies non, cursus eu diam.')
d.add_space(15)
table2 = [['Example']*8]*5
d.add_table(table2, col_widths='uniform', style='table2')
d.add_space(2)
d.add_section('Example table with no header', style='caption')

# Saving document as PDF
d.save()