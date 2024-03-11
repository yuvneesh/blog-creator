from flask_wtf import FlaskForm
from wtforms import Form as wtform
from wtforms import StringField, SubmitField, TextAreaField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired
import sqlite3

class ContentSectionForm(wtform):
    section_heading = StringField('Section Heading', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

class Scripts(wtform):
    scripts_id = StringField('Script-id')
    scripts_async = BooleanField('async')
    scripts_link = StringField('Script-link')

class Stylesheets(wtform):
    stylesheets_id = StringField('Stylesheet-id')
    stylesheets_link = StringField('Stylesheet-link')

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    scripts = FieldList(FormField(Scripts), min_entries=1)
    add_scripts_button = SubmitField("Add script")
    stylesheets = FieldList(FormField(Stylesheets), min_entries=1)
    add_stylesheets_button = SubmitField("Add stylesheet")
    sections = FieldList(FormField(ContentSectionForm), min_entries=1)
    add_section = SubmitField(label='Add Section')
    submit = SubmitField(label='Submit')

    def to_database(self, dbString: str) -> bool:
        """Push the blog to database
        
        Args:
            dbString (str): The connection string of the database
        Returns:
            True if the query was successful.
        """
        
        cursor = None
        try:
            cursor = sqlite3.connect(dbString).cursor()
        except:
            print("Database connection failed")

        if cursor:
            try:
                cursor.execute("INSERT INTO BLOGS (TITLE, SCRIPTS, STYLESHEETS, SECTIONS) VALUES (?, ?, ?, ?)", (self.title.data, self.scripts.data, self.stylesheets.data, self.sections_builder(), ))
            except Exception as ex:
                print(ex)
            finally:
                cursor.connection.commit()
                cursor.close()
                return True
            
        return False
    
    def sections_builder(self) -> str:
        """Build a string with all the sections"""
        sections_string = ""
        for section in self.sections.data:
            sections_string += section["section_heading"]
            sections_string += "\n"
            sections_string += section["content"]
            sections_string += "\n\n"
        return sections_string