from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from copy import deepcopy
from PIL import Image
import pandas as pd
import numpy as np

class Document:
    def __init__(self, name='document.pdf', width=letter[0], height=letter[1], margin_top = inch, margin_left = inch, 
                 margin_right = inch, margin_bottom = inch):
        """
        Initialize a Document instance for PDF generation.

        :param name: The name of the PDF file to be created (default is 'document.pdf').
        :param width: The width of the document page (default is width of the letter size).
        :param height: The height of the document page (default is height of the letter size).
        :param margin_top: The top margin of the document page (default is 1 inch).
        :param margin_left: The left margin of the document page (default is 1 inch).
        :param margin_right: The right margin of the document page (default is 1 inch).
        :param margin_bottom: The bottom margin of the document page (default is 1 inch).
        """
        self.name = name
        self.width = width
        self.height = height
        self.page = canvas.Canvas(name, pagesize=(width, height))
        self.margin_top = margin_top
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_bottom = margin_bottom

        self.current_height = 0
        self.page_count = False
        self.page_number = 1

        self.style_list = {}
        self._initialize_styles()
        self.table_style_list = {}
        self._initialize_table_styles()
        self.template_images = {}

    def _initialize_styles(self):
        """
        Set up the default styles for paragraphs in the document.

        Initializes styles for different types of text content:
        - Title
        - Paragraph
        - Page Number

        Styles are added to `self.style_list` with predefined attributes for font, size, alignment, and leading.
        """
        self.style_list['title'] = ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=14, alignment=0, 
                                                  leading=14, encoding="utf-8")
        self.style_list['paragraph'] = ParagraphStyle("Paragraph", fontName="Helvetica", fontSize=12, alignment=4, 
                                                      leading=12, encoding="utf-8")
        self.style_list['page_number'] = ParagraphStyle("Page Number", fontName="Helvetica", fontSize=12, alignment=1, 
                                                        leading=12, encoding="utf-8")

    def _initialize_table_styles(self):
        """
        Set up the default styles for tables in the document.

        Initializes table styles for:
        - Tables with headers
        - Tables without headers

        Styles are added to `self.table_style_list` with attributes for font, color, background, grid, and header.
        """
        self.table_style_list['table'] = {
            'header': True,
            'fontName': 'Helvetica-Bold',
            'fontSize': 8,
            'textColor': (0, 0, 0),
            'backgroundColor': (1, 1, 1),
            'gridColor': (0, 0, 0),
            'gridSize': 1,
            'headerColor': (0.5, 0.5, 0.5),
            'headerTextColor': (1, 1, 1)
        }
        self.table_style_list['no_header'] = {
            'header': False,
            'fontName': 'Helvetica-Bold',
            'fontSize': 8,
            'textColor': (0, 0, 0),
            'backgroundColor': (1, 1, 1),
            'gridColor': (0, 0, 0),
            'gridSize': 1,
            'headerColor': (1, 1, 1),
            'headerTextColor': (0, 0, 0)
        }

    def save(self):
        """
        Save the current document as a PDF file.
        """
        self.new_page()
        self.page.save()


    def new_page(self):
        """
        Generate a new page in the document.

        This method performs several actions:
        - Adds the current page number to the page if enabled.
        - Inserts template images on the page if there are any.
        - Saves the current state of the page and starts a new one.
        - Resets the current height to zero and increments the page number if page counting is enabled.
        """
        # Add the current page number to the page
        self._add_page_number()

        # Insert template images on the page if there are any
        for i in self.template_images:
            img = self.template_images[i]
            self.add_image(file=img['file'], size_proportions = img['size_proportions'], width = img['width'], 
                           height = img['height'], position='absolute', posx = img['posx'], posy = img['posy'], 
                           axisx = img['axisx'], axisy = img['axisy'])

        # Save the current page state and start a new page
        self.page.saveState()
        self.page.showPage()

        # Reset the height for the new page and update the page number if counting is enabled
        self.current_height = 0
        if self.page_count:
            self.page_number += 1

    def _add_page_number(self):
        """
        Add the current page number to the page if page counting is enabled.

        This method:
        - Checks if page numbering is enabled via `self.page_count`.
        - Creates a Paragraph object with the current page number.
        - Calculates the width and height of the page number text.
        - Draws the page number centered at the bottom of the page.
        """
        if self.page_count:
            page_number_text = Paragraph(str(self.page_number), self.style_list['page_number'])
            w_title, h_title = page_number_text.wrap(self.width, self.height)
            x_position = (self.width - w_title) / 2
            y_position = self.margin_bottom / 2
            page_number_text.drawOn(self.page, x_position, y_position)

    def toggle_page_count(self, page_number = None, set = None):
        """
        Toggle the automatic writing of page numbers and optionally set the current page number.

        :param page_number: The page number to set if page numbering is enabled. If None, retains the current page number.
        :param set: Boolean flag to turn page numbering on or off. If None, toggles the current state.

        This method:
        - Toggles the page numbering between True or False or sets it manually.
        - Sets the `page_number` to the provided value if `page_number` is not None.
        """
        self.page_count = not self.page_count if set is None else set
        self.page_number = page_number if page_number is not None else self.page_number

    def verify_page_break(self):
        """
        Check if a page break is needed and start a new page if necessary.

        This method calculates whether the current content will exceed the page height,
        considering margins. If so, it triggers a new page to be started.
        """
        if self.current_height+self.margin_top + self.margin_bottom > self.height:
            self.new_page()

    def add_section(self, text='Text', style = 'paragraph'):
        """
        Add a specified section to the document.

        This method:
        - Validates that the provided style exists in `self.style_list`.
        - Converts the text into a string and attempts to add it to the current page.
        - Checks if the text fits on the current page or needs to be split across pages.
        - Handles pagination if the text exceeds the available space on the current page.

        :param text: The text content of the section. Defaults to 'Text'.
        :param style: The style to apply to the text. Must be a key in `self.style_list`. Defaults to 'paragraph'.
        """

        # Validate parameters
        if style not in self.style_list:
            raise ValueError(f"Style '{style}' is not defined in style_list.")

        self.verify_page_break()

        text = str(text)
        sent = False
        has_split = False
        pointer = len(text.split(' ')) - 1

        # Verify if it's necessary to split text into different pages
        while not sent:
            title = Paragraph(text, self.style_list[style])
            w_title, h_title = title.wrap(self.width - self.margin_left - self.margin_right, self.height)

            page_break_needed  = self.current_height+self.margin_top + self.margin_bottom +h_title > self.height

            if not page_break_needed :
                # Send text
                title.drawOn(self.page, self.margin_left, self.height - self.margin_top - self.current_height - h_title)
                self.current_height += h_title
                sent = True

                if has_split:
                    # Send the rest of the split text
                    new_text = text.split(' ')[pointer+1:]
                    new_text = " ".join(new_text)
                    self.new_page()
                    self.add_section(text = new_text, style = style )
            else:
                # Split text and try to send again
                if pointer > 0:
                    # Split the text to make it smaller
                    has_split = True
                    text_split = text.split(' ')[:pointer]
                    text = " ".join(text_split)
                    pointer -= 1
                else:
                    # Margin too small, add a new page and try again
                    has_split = False
                    pointer = len(text.split(' ')) - 1
                    self.new_page()

    def add_sections(self, text='Text', style = 'paragraph'): 
        """
        Add a specified section to the document, creating new lines whenever `\n` is used.

        :param text: The text content of the section. 
        :param style: The style to apply to the text (must be a key in self.style_list).
        """
        texts = text.split('\n')
        for i in texts:
            self.add_section(text=i, style=style)

    def add_title(self, text='Title'):
        """
        Add a title section to the document with default styling.

        :param text: The text content to be used as the title. Defaults to 'Title'.
        """
        self.add_section(text=text, style = 'title')

    def title_config(self, fontName="Helvetica-Bold", fontSize=14, alignment=0, leading=None, textColor=(0,0,0)):
        """
        Change the default parameters for title generation.

        Updates the default styling for title sections in the document. This includes
        setting the font name, font size, alignment, leading, and text color.

        :param fontName: The font name to use for the title. Defaults to "Helvetica-Bold".
        :param fontSize: The font size to use for the title. Defaults to 14.
        :param alignment: The text alignment for the title. Defaults to 0 (left-aligned).
        :param leading: The line spacing (leading) for the title. If None, defaults to fontSize.
        :param textColor: The color of the text as an RGB tuple. Defaults to (0, 0, 0) (black).
        """
        self.style_list['title'] = ParagraphStyle("Title", fontName=fontName, fontSize=fontSize, alignment=alignment, 
                                                  leading=fontSize if leading is None else leading, encoding="utf-8", 
                                                  textColor=textColor)
    
    def add_paragraph(self, text='Paragraph'):
        """
        Add a paragraph to the document with default styling.

        :param text: The text content of the paragraph. Defaults to 'Paragraph'.
        """
        self.add_section(text=text, style = 'paragraph')

    def paragraph_config(self, fontName="Helvetica", fontSize=12, alignment=4, leading = None, textColor=(0,0,0)):
        """
        Change the default parameters for paragraph generation.

        Updates the default styling for paragraph sections in the document. This includes
        setting the font name, font size, alignment, leading, and text color.

        :param fontName: The font name to use for the paragraph. Defaults to "Helvetica".
        :param fontSize: The font size to use for the paragraph. Defaults to 12.
        :param alignment: The text alignment for the paragraph. Defaults to 4 (justified).
        :param leading: The line spacing (leading) for the paragraph. If None, defaults to fontSize.
        :param textColor: The color of the text as an RGB tuple. Defaults to (0, 0, 0) (black).
        """
        self.style_list['paragraph'] = ParagraphStyle("Paragraph", fontName=fontName, fontSize=fontSize, alignment=alignment, 
                                                      leading=fontSize if leading is None else leading, encoding="utf-8", 
                                                      textColor=textColor)

    def style_config(self, name='newStyle', fontName="Helvetica", fontSize=12, alignment=0, leading = None, textColor=(0,0,0)):
        """
        Create a new style to use when desired.

        Adds a new style to the style list with the specified parameters. This style can be
        applied to sections of the document as needed.

        :param name: The name of the new style. Defaults to 'newStyle'.
        :param fontName: The font name to use for the new style. Defaults to "Helvetica".
        :param fontSize: The font size to use for the new style. Defaults to 12.
        :param alignment: The text alignment for the new style. Defaults to 0 (left-aligned).
        :param leading: The line spacing (leading) for the new style. If None, defaults to fontSize.
        :param textColor: The color of the text as an RGB tuple. Defaults to (0, 0, 0) (black).
        """
        self.style_list[name] = ParagraphStyle(name, fontName=fontName, fontSize=fontSize, alignment=alignment, 
                                               leading=fontSize if leading is None else leading, encoding="utf-8", 
                                               textColor=textColor)

    def add_space(self, height=12):
        """
        Add space between lines.

        Increases the current height of the document by the specified amount to create
        vertical space between lines or sections.

        :param height: The height of the space to add. Defaults to 12.
        """
        self.current_height += height
    
    def add_image(self, file, size_proportions = 1, width = 1, height = 1, position='default', posx = 0, posy = 0, axisx = 'left', axisy = 'top'):
        """
        Add an image to the document.

        This method:
        - Verifies if a page break is needed before adding the image.
        - Validates the parameters for size proportions, width, height, and position.
        - Opens the image file and scales the image according to the given proportions and dimensions.
        - Determines the positioning of the image based on the specified positioning method `position`.
        - Adds the image to the page at the calculated position.

        :param file: Path to the image file.
        :param size_proportions: Scaling factor for the image size.
        :param width: Width factor for the image.
        :param height: Height factor for the image.
        :param position: Positioning of the image ('center', 'absolute', or 'default').
        :param posx: X coordinate for absolute positioning.
        :param posy: Y coordinate for absolute positioning.
        :param axisx: Horizontal alignment for absolute positioning ('left', 'center', 'right').
        :param axisy: Vertical alignment for absolute positioning ('top', 'center', 'bottom').
        """

        self.verify_page_break()
        
        # Validate parameters
        if size_proportions <= 0 or width <= 0 or height <= 0:
            raise ValueError("Size proportions, width, and height must be positive values.")
        
        if position not in ['center', 'absolute', 'default']:
            raise ValueError("Position must be 'center', 'absolute', or 'default'.")

         # Open the image
        try:
            with Image.open(file) as img:
                img_width, img_height = img.size
        except IOError:
            raise FileNotFoundError(f"Cannot open image file: {file}")
        
        img_width *= size_proportions * width
        img_height *= size_proportions * height

        # Center of line
        if position == 'center':
            left_margin = self.width/2 - img_width/2
            bottom_margin = self.height - self.margin_top - self.current_height - img_height
        # Absolute position on page
        elif position == 'absolute':
            left_margin, bottom_margin = self._set_absolute_positions(axisx, axisy, img_width, img_height, posx, posy)
        # Default 
        else:
            left_margin = self.margin_left
            bottom_margin = self.height - self.margin_top - self.current_height - img_height

        # Add the image to the page
        self.page.drawImage(file, left_margin, bottom_margin, img_width, img_height)
        self.current_height += img_height
    
    def add_table(self, data, col_widths = None, style='table', position='center', wrap=True):
        """
        Add a table to the document.

        This method:
        - Verifies if a page break is needed before adding the table.
        - Converts data from a DataFrame or ndarray to a list of lists if necessary.
        - Applies the specified table style to format the table.
        - Wraps text in table cells if the `wrap` parameter is set to True.
        - Determines the appropriate column widths and page breaks based on the table's size.
        - Adds the table to the document and handles pagination if the table does not fit on one page.

        :param data: The data to be displayed in the table. Can be a list of lists, a pandas DataFrame, or a numpy ndarray.
        :param col_widths: Column widths for the table. If 'uniform', columns are equally spaced. Defaults to None.
        :param style: The style to apply to the table (must be a key in `self.table_style_list`). Defaults to 'table'.
        :param position: Positioning of the table on the page. Can be 'center' or 'default'. Defaults to 'center'.
        :param wrap: If True, text in table cells will wrap to new lines if too large. Defaults to True.
        """
        self.verify_page_break()

        if isinstance(data, pd.DataFrame):
            columns = data.columns.tolist()
            data = data.values.tolist()
            data = [columns] + data
        
        if isinstance(data, np.ndarray):
            data = data.tolist()

        data = [row[:] for row in data]

        table_style_dict = self.table_style_list[style]
        table_style = self.generate_table(table_style_dict)
        
        data_send = deepcopy(data)
        
        # Makes text wrap to new line when too large
        if wrap:
            style_header = ParagraphStyle("Header", fontName = table_style_dict['fontName'], fontSize = table_style_dict['fontSize'], alignment=1, leading= table_style_dict['fontSize']+2, encoding="utf-8", textColor=table_style_dict['headerTextColor'])
            style_text = ParagraphStyle("Table", fontName = table_style_dict['fontName'], fontSize = table_style_dict['fontSize'], alignment=1, leading= table_style_dict['fontSize']+2, encoding="utf-8", textColor=table_style_dict['textColor'])
            
            for i in range(len(data)):
                for j in range(len(data[i])):
                    if i==0 and table_style_dict['header']:
                        data_send[i][j] = Paragraph(str(data[i][j]), style_header)
                    else:
                        data_send[i][j] = Paragraph(str(data[i][j]), style_text)
        
        # Divides columns equally if width was set to uniform
        if col_widths == 'uniform':
            n_cols = len(data[0])
            total_width = self.width - self.margin_left - self.margin_right
            col_widths = total_width / n_cols
        
        pointer = len(data)
        sent = False

        # Verify if it's necessary to split text into different pages
        while not sent: 

            table = Table(data_send[:pointer], colWidths=col_widths)
            table.setStyle(table_style)
            w_table, h_table = table.wrapOn(self.page, 0, 0)
            total_current_height = self.margin_top + self.current_height + h_table
            limit = self.height - self.margin_bottom

            # Too long to be sent in its current form
            if total_current_height > limit:
                if pointer > 1:
                    # Reduce the size of the table and try to send again
                    pointer -= 1
                else:
                    # Make another page and try to send everything again
                    self.new_page()
                    pointer = len(data_send)
            # Can be sent in its current form
            else:
                sent = True

                if position == 'default':
                    left_margin = self.margin_left
                else:
                    left_margin = (self.width - w_table)/2
                
                # If it can only display the header in this page, don't display it and make another page
                if pointer == 1 and len(data) > 1 and table_style_dict['header']:
                    self.new_page()
                else:
                    table.drawOn(self.page, left_margin, self.height - self.margin_top - self.current_height - h_table)
                    self.current_height += h_table
                    
                # Keep making the table on the other page
                if pointer != len(data_send):
                    # If it has a header, copy the header on every page until the table is complete
                    if table_style_dict['header']:
                        self.add_table(data = [data[0]]+data[pointer:], col_widths=col_widths, style=style, position=position, wrap=wrap)
                    else:
                        self.add_table(data = data[pointer:], col_widths=col_widths, style=style, position=position, wrap=wrap)
    
    def table_style(self, name='table', fontName='Helvetica-Bold', fontSize=8, textColor = (0,0,0), backgroundColor=(1,1,1), gridColor = (0,0,0), gridSize = 1, header=True, headerColor=(0.5,0.5,0.5), headerTextColor=(1,1,1)):
        """
        Change configurations of some table style.

        Updates the style settings for tables, including font, colors, grid size, and header options.
        The updated style can be applied to tables to customize their appearance.

        :param name: The name of the table style to update. Defaults to 'table'.
        :param fontName: The font name for table text. Defaults to 'Helvetica-Bold'.
        :param fontSize: The font size for table text. Defaults to 8.
        :param textColor: The color of the table text as an RGB tuple. Defaults to (0,0,0) (black).
        :param backgroundColor: The background color of the table as an RGB tuple. Defaults to (1,1,1) (white).
        :param gridColor: The color of the grid lines as an RGB tuple. Defaults to (0,0,0) (black).
        :param gridSize: The size of the grid lines. Defaults to 1.
        :param header: Whether the table has a header. Defaults to True.
        :param headerColor: The background color of the header as an RGB tuple. Defaults to (0.5,0.5,0.5) (grey).
        :param headerTextColor: The color of the header text as an RGB tuple. Defaults to (1,1,1) (white).
        """
        self.table_style_list[name] = {
            'header': header,
            'fontName': fontName,
            'fontSize': fontSize,
            'textColor': textColor,
            'backgroundColor': backgroundColor,
            'gridColor' : gridColor,
            'gridSize' : gridSize,
            'headerColor': headerColor,
            'headerTextColor': headerTextColor
        }
     
    def generate_table(self, style):
        """
        Generate a table from a table style dictionary.

        Creates a `TableStyle` object based on the provided style dictionary, applying 
        alignment, font settings, colors, and grid options. Optionally, it can apply 
        header styling if specified in the style dictionary.

        :param style: A dictionary containing table style settings, including alignment, font, colors, 
                    grid options, and header settings.

        :return: A `TableStyle` object configured according to the provided style settings.
        """
        base_styles = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), style['gridSize'], style['gridColor']),
            ('FONTNAME', (0, 0), (-1, -1), style['fontName']),
            ('FONTSIZE', (0, 0), (-1, -1), style['fontSize']),
            ('BACKGROUND', (0, 0), (-1, -1), style['backgroundColor']),
            ('TEXTCOLOR', (0, 0), (-1, -1), style['textColor']),
        ]

        if style['header']:
            extra_styles = [
                ('BACKGROUND', (0, 0), (-1, -1), style['headerColor']),
                ('TEXTCOLOR', (0, 0), (-1, -1), style['headerTextColor']),
                ('BACKGROUND', (0, 1), (-1, -1), style['backgroundColor']),
                ('TEXTCOLOR', (0, 1), (-1, -1), style['textColor']),
            ]
            base_styles.extend(extra_styles)
            
        return TableStyle(base_styles)
    
    def add_template_image(self, name, file, size_proportions = 1, width = 1, height = 1, posx = 0, posy = 0, axisx = 'left', axisy = 'top'):
        """
        Add template images that will be used on every page when specified.

        Registers an image to be used as a template on every page. It can be a header, footer or logo 
        for example. You can specify its size, position, and alignment relative to the page.

        :param name: The name of the template image for identification.
        :param file: The file path of the image to be used as a template.
        :param size_proportions: The proportional scaling factor for the image. Defaults to 1.
        :param width: The width of the image. Defaults to 1.
        :param height: The height of the image. Defaults to 1.
        :param posx: The x-coordinate position of the image. Defaults to 0.
        :param posy: The y-coordinate position of the image. Defaults to 0.
        :param axisx: The horizontal alignment of the image ('left', 'center', 'right'). Defaults to 'left'.
        :param axisy: The vertical alignment of the image ('top', 'middle', 'bottom'). Defaults to 'top'.
        """
        self.template_images[name] = {
            'file': file,
            'size_proportions': size_proportions, 
            'width': width,
            'height': height,
            'posx': posx,
            'posy': posy,
            'axisx': axisx,
            'axisy': axisy
        }

    def remove_template_image(self, name):
        """
        Remove a template image.

        Deletes the specified template image from the list of images that will be used on every page.

        :param name: The name of the template image to remove.
        """
        self.template_images.pop(name)

    def _set_absolute_positions(self, axisx, axisy, img_width, img_height, posx, posy):
        """
        Calculate margins for images to determine their absolute positions on the page.

        Computes the left and bottom margins for positioning an image based on its width,
        height, and specified alignment relative to the page dimensions. The alignment is 
        determined by `axisx` and `axisy`, which specify how the image should be positioned 
        horizontally and vertically.

        :param axisx: The horizontal alignment of the image. Can be 'left', 'center', or 'right'.
        :param axisy: The vertical alignment of the image. Can be 'top', 'center', or 'bottom'.
        :param img_width: The width of the image.
        :param img_height: The height of the image.
        :param posx: The horizontal offset from the alignment point.
        :param posy: The vertical offset from the alignment point.

        :return: A tuple (left_margin, bottom_margin) representing the margins to apply 
                for positioning the image.
        """
        if axisx == 'right':
            left_margin = self.width - img_width - posx
        elif axisx == 'center':
            left_margin = (self.width - img_width)/2 + posx
        else:
            left_margin = posx

        if axisy == 'bottom':
            bottom_margin = posy
        elif axisy == 'center':
            bottom_margin = (self.height - img_height)/2 - posy
        else:
            bottom_margin = self.height - img_height - posy
        
        return left_margin, bottom_margin