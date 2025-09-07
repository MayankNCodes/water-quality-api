from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
import datetime

class WaterQualityPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
    
    def generate_report(self, sample_data):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        title = Paragraph("Water Quality Analysis Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Sample Information Section
        sample_info_title = Paragraph("Sample Information", self.heading_style)
        story.append(sample_info_title)
        
        sample_info_data = [
            ['Sample ID:', sample_data['sample_id']],
            ['Sampling Date:', sample_data['sampling_date']],
            ['Location:', f"Lat: {sample_data['latitude']}, Long: {sample_data['longitude']}"],
            ['Well Depth:', f"{sample_data['well_depth']} m"],
            ['Report Generated:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]
        
        sample_info_table = Table(sample_info_data, colWidths=[2*inch, 3*inch])
        sample_info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(sample_info_table)
        story.append(Spacer(1, 30))
        
        # Water Quality Indices Section
        indices_title = Paragraph("Calculated Water Quality Indices", self.heading_style)
        story.append(indices_title)
        
        indices_data = [
            ['Index', 'Value', 'Description'],
            ['HMPI', f"{sample_data['hmpi']:.2f}" if sample_data['hmpi'] else 'N/A', 'Heavy Metal Pollution Index'],
            ['HPI', f"{sample_data['hpi']:.2f}" if sample_data['hpi'] else 'N/A', 'Health Risk Index'],
            ['HEI', f"{sample_data['hei']:.2f}" if sample_data['hei'] else 'N/A', 'Heavy Metal Evaluation Index'],
            ['HCI', f"{sample_data['hci']:.2f}" if sample_data['hci'] else 'N/A', 'Heavy Metal Contamination Index'],
            ['Cd', f"{sample_data['cd']:.2f}" if sample_data['cd'] else 'N/A', 'Contamination Degree'],
            ['PI', f"{sample_data['pi']:.2f}" if sample_data['pi'] else 'N/A', 'Pollution Index'],
            ['PLI', f"{sample_data['pli']:.2f}" if sample_data['pli'] else 'N/A', 'Pollution Load Index'],
        ]
        
        indices_table = Table(indices_data, colWidths=[1.5*inch, 1*inch, 2.5*inch])
        indices_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(indices_table)
        story.append(Spacer(1, 30))
        
        # Interpretation Section
        interpretation_title = Paragraph("Index Interpretation Guidelines", self.heading_style)
        story.append(interpretation_title)
        
        interpretation_text = """
        <b>HMPI (Heavy Metal Pollution Index):</b><br/>
        • &lt; 100: Low pollution<br/>
        • 100-200: Medium pollution<br/>
        • &gt; 200: High pollution<br/><br/>
        
        <b>HPI (Health Risk Index):</b><br/>
        • &lt; 100: Acceptable for drinking<br/>
        • 100-300: Slightly affected<br/>
        • &gt; 300: Highly affected<br/><br/>
        
        <b>PLI (Pollution Load Index):</b><br/>
        • PLI &lt; 1: No pollution<br/>
        • PLI = 1: Baseline pollution<br/>
        • PLI &gt; 1: Polluted<br/>
        """
        
        interpretation_para = Paragraph(interpretation_text, self.styles['Normal'])
        story.append(interpretation_para)
        
        # Footer
        story.append(Spacer(1, 50))
        footer_text = f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Water Quality Analysis System"
        footer = Paragraph(footer_text, ParagraphStyle('Footer', 
                                                     parent=self.styles['Normal'],
                                                     fontSize=8,
                                                     alignment=TA_CENTER,
                                                     textColor=colors.grey))
        story.append(footer)
        
        doc.build(story)
        buffer.seek(0)
        return buffer
