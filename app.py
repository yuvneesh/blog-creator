from flask import Flask, render_template, request, redirect, url_for
from form_handling import BlogPostForm
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.dbString = os.getenv('DB_STRING')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = BlogPostForm()
    if request.method == 'POST':

        if form.add_section.data:
            form.sections.append_entry()
            return render_template("form.html", form=form)

        if form.add_scripts_button.data:
            form.scripts.append_entry()
            return render_template("form.html", form=form)

        if form.add_stylesheets_button.data:
            form.stylesheets.append_entry()
            return render_template("form.html", form=form)
        
        elif form.submit.data:
            if form.validate():
                form.to_database(app.dbString)
                return redirect(url_for('index')) # Redirect or display a success message

            
    return render_template("form.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
