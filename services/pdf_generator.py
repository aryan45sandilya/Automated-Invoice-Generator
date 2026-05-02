from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from datetime import datetime
import os


class PDFGenerator:
    """Service for generating professional PDF invoices"""
    
    def __init__(self, config):
        self.config = config
        self.company_name = config.get('COMPANY_NAME', 'Your Company')
        self.company_email = config.get('COMPANY_EMAIL', 'company@example.com')
        self.company_phone = config.get('COMPANY_PHONE', '+1-234-567-8900')
        self.company_address = config.get('COMPANY_ADDRESS', '123 Business St')
        self.currency_symbol = config.get('CURRENCY_SYMBOL', '$')
    
    def generate_invoice(self, invoice, client, items, filename):
        """
        Generate a professional invoice PDF
        
        Args:
            invoice: Invoice model instance
            client: Client model instance
            items: List of InvoiceItem instances
            filename: Output PDF filename
        """
        # Create the PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Container for PDF elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12
        )
        
        normal_style = styles['Normal']
        
        # Title
        title = Paragraph("INVOICE", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Company and Client Info Table
        info_data = [
            [
                Paragraph(f"<b>{self.company_name}</b><br/>{self.company_address}<br/>{self.company_phone}<br/>{self.company_email}", normal_style),
                Paragraph(f"<b>Invoice #:</b> {invoice.invoice_number}<br/><b>Date:</b> {invoice.date.strftime('%B %d, %Y')}<br/><b>Due Date:</b> {invoice.due_date.strftime('%B %d, %Y')}<br/><b>Status:</b> <font color='{'green' if invoice.status == 'Paid' else 'red'}'>{invoice.status}</font>", normal_style)
            ]
        ]
        
        info_table = Table(info_data, colWidths=[3.5*inch, 3.5*inch])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Bill To Section
        bill_to = Paragraph(f"<b>BILL TO:</b>", heading_style)
        elements.append(bill_to)
        
        client_info = f"<b>{client.name}</b><br/>"
        if client.company:
            client_info += f"{client.company}<br/>"
        if client.address:
            client_info += f"{client.address}<br/>"
        client_info += f"{client.email}<br/>"
        if client.phone:
            client_info += f"{client.phone}<br/>"
        if client.gstin:
            client_info += f"<b>GSTIN:</b> {client.gstin}"
        
        client_para = Paragraph(client_info, normal_style)
        elements.append(client_para)
        elements.append(Spacer(1, 0.3*inch))
        
        # Items Table
        items_data = [['#', 'Description', 'Qty', 'Price', 'Total']]
        
        for idx, item in enumerate(items, 1):
            items_data.append([
                str(idx),
                item.description,
                str(item.quantity),
                f"{self.currency_symbol}{item.price:.2f}",
                f"{self.currency_symbol}{item.total:.2f}"
            ])
        
        items_table = Table(items_data, colWidths=[0.5*inch, 3.5*inch, 0.8*inch, 1.2*inch, 1.2*inch])
        items_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Body
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(items_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Totals Table
        totals_data = [
            ['Subtotal:', f"{self.currency_symbol}{invoice.subtotal:.2f}"],
            [f'Tax ({invoice.tax_rate}%):', f"{self.currency_symbol}{invoice.tax_amount:.2f}"],
        ]
        
        if invoice.discount > 0:
            totals_data.append(['Discount:', f"-{self.currency_symbol}{invoice.discount:.2f}"])
        
        totals_data.append(['<b>TOTAL:</b>', f"<b>{self.currency_symbol}{invoice.total_amount:.2f}</b>"])
        
        # Convert to Paragraphs for bold text
        totals_data_formatted = []
        for row in totals_data:
            totals_data_formatted.append([
                Paragraph(row[0], normal_style),
                Paragraph(row[1], normal_style)
            ])
        
        totals_table = Table(totals_data_formatted, colWidths=[5.3*inch, 1.9*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('TOPPADDING', (0, -1), (-1, -1), 12),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#34495E')),
        ]))
        
        elements.append(totals_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Notes
        if invoice.notes:
            notes_heading = Paragraph("<b>Notes:</b>", heading_style)
            elements.append(notes_heading)
            notes_text = Paragraph(invoice.notes, normal_style)
            elements.append(notes_text)
            elements.append(Spacer(1, 0.2*inch))
        
        # Terms
        if invoice.terms:
            terms_heading = Paragraph("<b>Terms & Conditions:</b>", heading_style)
            elements.append(terms_heading)
            terms_text = Paragraph(invoice.terms, normal_style)
            elements.append(terms_text)
            elements.append(Spacer(1, 0.2*inch))
        
        # Footer
        elements.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        footer = Paragraph(
            f"Thank you for your business!<br/>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            footer_style
        )
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        
        return filename
    
    def generate_report(self, invoices, filename, report_type='summary'):
        """
        Generate a report PDF
        
        Args:
            invoices: List of Invoice instances
            filename: Output PDF filename
            report_type: Type of report (summary, detailed)
        """
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"Invoice Report - {datetime.now().strftime('%B %Y')}", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary statistics
        total_revenue = sum(inv.total_amount for inv in invoices)
        paid_invoices = [inv for inv in invoices if inv.status == 'Paid']
        pending_invoices = [inv for inv in invoices if inv.status == 'Pending']
        
        summary_data = [
            ['Total Invoices:', str(len(invoices))],
            ['Total Revenue:', f"{self.currency_symbol}{total_revenue:.2f}"],
            ['Paid Invoices:', str(len(paid_invoices))],
            ['Pending Invoices:', str(len(pending_invoices))],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Invoice list
        if report_type == 'detailed':
            invoice_data = [['Invoice #', 'Client', 'Date', 'Amount', 'Status']]
            
            for inv in invoices:
                invoice_data.append([
                    inv.invoice_number,
                    inv.client.name,
                    inv.date.strftime('%Y-%m-%d'),
                    f"{self.currency_symbol}{inv.total_amount:.2f}",
                    inv.status
                ])
            
            invoice_table = Table(invoice_data, colWidths=[1.5*inch, 2*inch, 1.2*inch, 1.2*inch, 1*inch])
            invoice_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(invoice_table)
        
        doc.build(elements)
        return filename
