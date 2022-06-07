# Importing Required Libraries
import sublime_plugin
import sublime
import shutil
import json
import os


# Initilise Plugin
def plugin_init():
    sublime_path = os.path.dirname(sublime.packages_path())
    sublime_user_path = os.path.join(sublime_path, "Packages", "User")
    plugin_data_path = os.path.join(sublime_user_path, "Competitive Programming Lite")
    os.makedirs(plugin_data_path, exist_ok=True)

    # Copy the Default Files
    if not os.path.exists(os.path.join(plugin_data_path, ".cpl_init")):
        # Build Folder
        plugin_build_path = os.path.join(plugin_data_path, "build")
        os.makedirs(plugin_build_path, exist_ok=True)
        for f in sublime.find_resources("*"):
            if f.startswith("Packages/Competitive Programming Lite/build/"):
                content = sublime.load_binary_resource(f)
                f_name = f.replace("Packages/Competitive Programming Lite/build/", "")
                if f.endswith(".build-json"):
                    f_name =  f_name[:-11] + ".sublime-build"
                with open(os.path.join(plugin_build_path, f_name), "wb") as f:
                    f.write(content)

        # Files Folder
        plugin_files_path = os.path.join(plugin_data_path, "files")
        os.makedirs(plugin_files_path, exist_ok=True)
        for f in sublime.find_resources("*"):
            if f.startswith("Packages/Competitive Programming Lite/files/"):
                content = sublime.load_binary_resource(f)
                f_name = f.replace("Packages/Competitive Programming Lite/files/", "")
                with open(os.path.join(plugin_files_path, f_name), "wb") as f:
                    f.write(content)

        # Languages Folder
        plugin_languages_path = os.path.join(plugin_data_path, "languages")
        os.makedirs(plugin_languages_path, exist_ok=True)
        for f in sublime.find_resources("*"):
            if f.startswith("Packages/Competitive Programming Lite/languages/"):
                content = sublime.load_binary_resource(f)
                f_name = f.replace("Packages/Competitive Programming Lite/languages/", "")
                with open(os.path.join(plugin_languages_path, f_name), "wb") as f:
                    f.write(content)
        
        # Sublime Folder
        plugin_sublime_path = os.path.join(plugin_data_path, "sublime")
        os.makedirs(plugin_sublime_path, exist_ok=True)

        # Templates Folder
        plugin_templates_path = os.path.join(plugin_data_path, "templates")
        os.makedirs(plugin_templates_path, exist_ok=True)
        for f in sublime.find_resources("*"):
            if f.startswith("Packages/Competitive Programming Lite/templates/"):
                content = sublime.load_binary_resource(f)
                f_name = f.replace("Packages/Competitive Programming Lite/templates/", "")
                with open(os.path.join(plugin_templates_path, f_name), "wb") as f:
                    f.write(content)
        
        # Successfully Initialized
        with open(os.path.join(plugin_data_path, ".cpl_init"), "w") as f:
            f.write("Do not delete this file")


# Command for Creating a File
class CpNewCommand(sublime_plugin.TextCommand):
    # Default run Command
    def run(self, edit, question, template):
        plugin_init()

        sublime_path = os.path.dirname(sublime.packages_path())
        sublime_user_path = os.path.join(sublime_path, "Packages", "User")
        plugin_data_path = os.path.join(sublime_user_path, "Competitive Programming Lite")
        plugin_path = plugin_data_path
        project_window = sublime.active_window()

        try:
            project_path = project_window.project_data()["folders"][0]["path"]
        except:
            sublime.error_message("Please Open a Folder First")
            return
        if not os.path.exists(project_path):
            sublime.error_message("Please Open a Valid Folder")
            return
        try:
            os.makedirs(os.path.join(project_path, ".cpl_files"), exist_ok=True)
        except:
            sublime.error_message("Unable to Create '.cpl_files' Folder")
            return

        # Handling Input Values
        if not (question.isdigit() and int(question)):
            question = "1"
        with open(os.path.join(plugin_path, "templates/templates.json"), "r") as f:
            language_templates = json.load(f)
        templates = {i: "{0} ({1})".format(j[0], j[1]) for i, j in language_templates.items()}
        if template in templates.values():
            template = list(templates.keys())[list(templates.values()).index(template)]
        else:
            template = "1"

        # Closing Old Tabs
        project_window.focus_group(0)
        [v.run_command("save") if v.file_name() else v.erase(edit, sublime.Region(0, v.size())) for v in project_window.views()]
        project_window.run_command("close_all")

        # Copying Solution Tester File
        if not (os.path.exists(os.path.join(project_path, ".cpl_files/solution_tester.py"))):
            shutil.copyfile(os.path.join(plugin_path, "files/solution_tester.py"), os.path.join(project_path, ".cpl_files/solution_tester.py"))

        # Copying Java Runner File
        if not (os.path.exists(os.path.join(project_path, ".cpl_files/java_runner.py"))):
            shutil.copyfile(os.path.join(plugin_path, "files/java_runner.py"), os.path.join(project_path, ".cpl_files/java_runner.py"))

        # Language Template Code
        template_name = language_templates[template][0]
        language_extension = language_templates[template][2]
        with open(os.path.join(plugin_path, "templates/{0}.{1}".format(template_name, language_extension)), "r") as f:
            language_template = f.read()

        # Generating CP Files
        if (os.path.exists(os.path.join(project_path, "{0}_{1}.{2}".format(question, template_name, language_extension)))):
            if sublime.ok_cancel_dialog("{0}_{1}.{2} already exists. Do you want to override the old file?".format(question, template_name, language_extension), "Yes"):
                with open(os.path.join(project_path, "{0}_{1}.{2}".format(question, template_name, language_extension)), "w") as f:
                    f.write(language_template.replace(r"{N}", str(question)))
        else:
            with open(os.path.join(project_path, "{0}_{1}.{2}".format(question, template_name, language_extension)), "w") as f:
                f.write(language_template.replace(r"{N}", str(question)))
        if not (os.path.exists(os.path.join(project_path, ".cpl_files/{0}.in.txt".format(question)))):
            with open(os.path.join(project_path, ".cpl_files/{0}.in.txt".format(question)), "w") as f:
                f.write("")
        if not (os.path.exists(os.path.join(project_path, ".cpl_files/{0}.out.txt".format(question)))):
            with open(os.path.join(project_path, ".cpl_files/{0}.out.txt".format(question)), "w") as f:
                f.write("")
        if not (os.path.exists(os.path.join(project_path, ".cpl_files/{0}.tst.txt".format(question)))):
            with open(os.path.join(project_path, ".cpl_files/{0}.tst.txt".format(question)), "w") as f:
                f.write("")

        # Setting CP Layout
        project_window.set_minimap_visible(False)
        project_window.set_sidebar_visible(False)
        project_window.run_command("set_layout", {"cells": [[0, 0, 1, 2], [1, 0, 2, 1], [1, 1, 2, 2]], "cols": [0.0, 0.8, 1.0], "rows": [0.0, 0.5, 1.0]})

        # Opening New Tabs
        project_window.focus_group(0)
        project_window.open_file(os.path.join(project_path, "{0}_{1}.{2}".format(question, language_templates[template][0], language_templates[template][2])))
        project_window.focus_group(1)
        project_window.open_file(os.path.join(project_path, ".cpl_files/{0}.in.txt".format(question)))
        project_window.focus_group(2)
        project_window.open_file(os.path.join(project_path, ".cpl_files/{0}.tst.txt".format(question)))
        project_window.focus_group(0)

        # Changing Build System
        with open(os.path.join(plugin_path, "build/build.json"), "r") as f:
            build_systems = json.load(f)

        project_window.run_command("set_build_system", {"file": "Packages/User/Competitive Programming Lite/build/{0}.sublime-build".format(build_systems[language_templates[template][2]])})

    # Getting Question Nummber and Template Input
    def input(self, args):
        if "question" not in args:
            return QuestionInputHandler()
        elif "template" not in args:
            return TemplateInputHandler()


# Command for Creating a Set of Files
class CpSetCommand(sublime_plugin.TextCommand):
    # Default run Command
    def run(self, edit, questions, template):
        plugin_init()

        sublime_path = os.path.dirname(sublime.packages_path())
        sublime_user_path = os.path.join(sublime_path, "Packages", "User")
        plugin_data_path = os.path.join(sublime_user_path, "Competitive Programming Lite")
        plugin_path = plugin_data_path
        project_window = sublime.active_window()

        try:
            project_path = project_window.project_data()["folders"][0]["path"]
        except:
            sublime.error_message("Please Open a Folder First")
            return
        if not os.path.exists(project_path):
            sublime.error_message("Please Open a Valid Folder")
            return
        try:
            os.makedirs(os.path.join(project_path, ".cpl_files"), exist_ok=True)
        except:
            sublime.error_message("Unable to Create '.cpl_files' Folder")
            return

        # Handling Input Values
        if not (questions.isdigit() and int(questions)):
            questions = "6"
        with open(os.path.join(plugin_path, "templates/templates.json"), "r") as f:
            language_templates = json.load(f)
        templates = {i: "{0} ({1})".format(j[0], j[1]) for i, j in language_templates.items()}
        if template in templates.values():
            template = list(templates.keys())[list(templates.values()).index(template)]
        else:
            template = "1"

        # Closing Old Tabs
        project_window.focus_group(0)
        [v.run_command("save") if v.file_name() else v.erase(edit, sublime.Region(0, v.size())) for v in project_window.views()]
        project_window.run_command("close_all")

        # Copying Solution Tester File
        if not (os.path.exists(os.path.join(project_path, ".cpl_files/solution_tester.py"))):
            shutil.copyfile(os.path.join(plugin_path, "files/solution_tester.py"), os.path.join(project_path, ".cpl_files/solution_tester.py"))

        # Copying Java Runner File
        if not (os.path.exists(os.path.join(project_path, ".cpl_files/java_runner.py"))):
            shutil.copyfile(os.path.join(plugin_path, "files/java_runner.py"), os.path.join(project_path, ".cpl_files/java_runner.py"))

        # Language Template Code
        template_name = language_templates[template][0]
        language_extension = language_templates[template][2]
        with open(os.path.join(plugin_path, "templates/{0}.{1}".format(template_name, language_extension)), "r") as f:
            language_template = f.read()

        # Generating CP Files
        override_flag = False
        for i in range(1, int(questions)+1):
            if (not override_flag) and (os.path.exists(os.path.join(project_path, "{0}_{1}.{2}".format(i, template_name, language_extension)))):
                choice = sublime.yes_no_cancel_dialog("{0}_{1}.{2} already exists. Do you want to override the old file?".format(i, template_name, language_extension), "Yes", "Yes to All")
                if int(choice) == 2:
                    override_flag = True
                if choice:
                    with open(os.path.join(project_path, "{0}_{1}.{2}".format(i, template_name, language_extension)), "w") as f:
                        f.write(language_template.replace(r"{N}", str(i)))
            else:
                with open(os.path.join(project_path, "{0}_{1}.{2}".format(i, template_name, language_extension)), "w") as f:
                    f.write(language_template.replace(r"{N}", str(i)))
            if not (os.path.exists(os.path.join(project_path, ".cpl_files/{0}.in.txt".format(i)))):
                with open(os.path.join(project_path, ".cpl_files/{0}.in.txt".format(i)), "w") as f:
                    f.write("")
            if not (os.path.exists(os.path.join(project_path, ".cpl_files/{0}.out.txt".format(i)))):
                with open(os.path.join(project_path, ".cpl_files/{0}.out.txt".format(i)), "w") as f:
                    f.write("")
            if not (os.path.exists(os.path.join(project_path, ".cpl_files/{0}.tst.txt".format(i)))):
                with open(os.path.join(project_path, ".cpl_files/{0}.tst.txt".format(i)), "w") as f:
                    f.write("")

        # Setting CP Layout
        project_window.set_minimap_visible(False)
        project_window.set_sidebar_visible(False)
        project_window.run_command("set_layout", {"cells": [[0, 0, 1, 2], [1, 0, 2, 1], [1, 1, 2, 2]], "cols": [0.0, 0.8, 1.0], "rows": [0.0, 0.5, 1.0]})

        # Opening New Tabs
        project_window.focus_group(0)
        project_window.open_file(os.path.join(project_path, "1_{0}.{1}".format(language_templates[template][0], language_templates[template][2])))
        project_window.focus_group(1)
        project_window.open_file(os.path.join(project_path, ".cpl_files/1.in.txt"))
        project_window.focus_group(2)
        project_window.open_file(os.path.join(project_path, ".cpl_files/1.tst.txt"))
        project_window.focus_group(0)

        # Changing Build System
        with open(os.path.join(plugin_path, "build/build.json"), "r") as f:
            build_systems = json.load(f)
        project_window.run_command("set_build_system", {"file": "Packages/User/Competitive Programming Lite/build/{0}.sublime-build".format(build_systems[language_templates[template][2]])})

    # Getting Total Questions and Template Input
    def input(self, args):
        if "questions" not in args:
            return QuestionsInputHandler()
        elif "template" not in args:
            return TemplateInputHandler()


# Command for Opening a File
class CpOpenCommand(sublime_plugin.TextCommand):
    # Default run Command
    def run(self, edit, question, template):
        plugin_init()

        sublime_path = os.path.dirname(sublime.packages_path())
        sublime_user_path = os.path.join(sublime_path, "Packages", "User")
        plugin_data_path = os.path.join(sublime_user_path, "Competitive Programming Lite")
        plugin_path = plugin_data_path
        project_window = sublime.active_window()

        try:
            project_path = project_window.project_data()["folders"][0]["path"]
        except:
            sublime.error_message("Please Open a Folder First")
            return
        if not os.path.exists(project_path):
            sublime.error_message("Please Open a Valid Folder")
            return
        try:
            os.makedirs(os.path.join(project_path, ".cpl_files"), exist_ok=True)
        except:
            sublime.error_message("Unable to Create '.cpl_files' Folder")
            return

        # Handling Input Values
        o_question, o_template = question, template
        if not (question.isdigit() and int(question)):
            question = "1"
        with open(os.path.join(plugin_path, "templates/templates.json"), "r") as f:
            language_templates = json.load(f)
        templates = {i: "{0} ({1})".format(j[0], j[1]) for i, j in language_templates.items()}
        if template in templates.values():
            template = list(templates.keys())[list(templates.values()).index(template)]
        else:
            template = "1"

        # Closing Old Tabs
        project_window.focus_group(0)
        [v.run_command("save") if v.file_name() else v.erase(edit, sublime.Region(0, v.size())) for v in project_window.views()]
        project_window.run_command("close_all")

        # Setting CP Layout
        project_window.set_minimap_visible(False)
        project_window.set_sidebar_visible(False)
        project_window.run_command("set_layout", {"cells": [[0, 0, 1, 2], [1, 0, 2, 1], [1, 1, 2, 2]], "cols": [0.0, 0.8, 1.0], "rows": [0.0, 0.5, 1.0]})

        # Opening New Tabs
        project_window.focus_group(0)
        if (os.path.exists(os.path.join(project_path, "{0}_{1}.{2}".format(question, language_templates[template][0], language_templates[template][2])))):
            project_window.open_file(os.path.join(project_path, "{0}_{1}.{2}".format(question, language_templates[template][0], language_templates[template][2])))
        elif sublime.ok_cancel_dialog("{0}_{1}.{2} does not exist. Do you want to create {0}_{1}.{2}?".format(question, language_templates[template][0], language_templates[template][2]), "Yes"):
            project_window.run_command("cp_new", {"question": o_question, "template": o_template})
            return
        else:
            project_window.run_command("cp_end")
            return
        project_window.focus_group(1)
        if not (os.path.exists(os.path.join(project_path, ".cpl_files/{0}.in.txt".format(question)))):
            with open(os.path.join(project_path, ".cpl_files/{0}.in.txt".format(question)), "w") as f:
                f.write("")
        project_window.open_file(os.path.join(project_path, ".cpl_files/{0}.in.txt".format(question)))
        project_window.focus_group(2)
        if not (os.path.exists(os.path.join(project_path, ".cpl_files/{0}.tst.txt".format(question)))):
            with open(os.path.join(project_path, ".cpl_files/{0}.tst.txt".format(question)), "w") as f:
                f.write("")
        project_window.open_file(os.path.join(project_path, ".cpl_files/{0}.tst.txt".format(question)))
        project_window.focus_group(0)

        # Changing Build System
        with open(os.path.join(plugin_path, "build/build.json"), "r") as f:
            build_systems = json.load(f)
        project_window.run_command("set_build_system", {"file": "Packages/User/Competitive Programming Lite/build/{0}.sublime-build".format(build_systems[language_templates[template][2]])})

    # Getting Question Nummber and Template Input
    def input(self, args):
        if "question" not in args:
            return QuestionInputHandler()
        elif "template" not in args:
            return TemplateInputHandler()


# Command for Exiting CP Mode
class CpEndCommand(sublime_plugin.TextCommand):
    # Default run Command
    def run(self, edit):
        plugin_init()

        sublime_path = os.path.dirname(sublime.packages_path())
        sublime_user_path = os.path.join(sublime_path, "Packages", "User")
        plugin_data_path = os.path.join(sublime_user_path, "Competitive Programming Lite")
        plugin_path = plugin_data_path

        project_window = sublime.active_window()

        # Closing All Tabs
        project_window.focus_group(0)
        [v.run_command("save") if v.file_name() else v.erase(edit, sublime.Region(0, v.size())) for v in project_window.views()]
        project_window.run_command("close_all")

        # Setting Default Layout
        project_window.set_minimap_visible(True)
        project_window.set_sidebar_visible(False)
        project_window.run_command("set_layout", {"cells": [[0, 0, 1, 1]], "cols": [0.0, 1.0], "rows": [0.0, 1.0]})

        # Changing Build System
        project_window.run_command("set_build_system", {"file": ""})


# Command for Adding a Template
class CpAddCommand(sublime_plugin.TextCommand):
    # Default run Command
    def run(self, edit, language, name):
        plugin_init()

        sublime_path = os.path.dirname(sublime.packages_path())
        sublime_user_path = os.path.join(sublime_path, "Packages", "User")
        plugin_data_path = os.path.join(sublime_user_path, "Competitive Programming Lite")
        plugin_path = plugin_data_path
        project_window = sublime.active_window()

        # Handling Input Values
        with open(os.path.join(plugin_path, "languages/languages.json"), "r") as f:
            languages_data = json.load(f)
        languages = {i: j[0] for i, j in languages_data.items()}
        if language in languages.values():
            language = list(languages.keys())[list(languages.values()).index(language)]
        else:
            sublime.error_message("Unknown Error")
            return
        if name == "":
            sublime.error_message("Empty Name")
            return
        elif all(c.isalnum() or c == ' ' for c in name) and not name.isspace():
            pass
        else:
            sublime.error_message("Invalid Name")
            return

        # Checking if Template Already Exists
        if os.path.exists(os.path.join(plugin_path, "templates/{0}.{1}".format(name, languages_data[language][1]))):
            sublime.error_message("Template with same name already exists.")
            return

        # Creating Template File
        with open(os.path.join(plugin_path, "templates/Default.{0}".format(languages_data[language][1])), "r") as f:
            default_value = f.read()
        with open(os.path.join(plugin_path, "templates/{0}.{1}".format(name, languages_data[language][1])), "w") as f:
            f.write(default_value)

        # Adding Template File
        with open(os.path.join(plugin_path, "templates/templates.json"), "r") as f:
            templates_data = json.load(f)
        templates_data[max([int(x) for x in templates_data.keys()])+1] = [name, languages_data[language][0], languages_data[language][1]]
        with open(os.path.join(plugin_path, "templates/templates.json"), "w") as f:
            f.write(json.dumps(templates_data, indent=4))

        # Opening Template File
        language_extension = languages_data[language][1]
        project_window.run_command("open_file", {"file": os.path.join(plugin_path, "templates/{0}.{1}".format(name, language_extension))})

    # Getting Language and Name Input
    def input(self, args):
        if "language" not in args:
            return LanguageInputHandler()
        elif "name" not in args:
            return NameInputHandler()


# Command for Editing a Template
class CpEditCommand(sublime_plugin.TextCommand):
    # Default run Command
    def run(self, edit, template):
        plugin_init()

        sublime_path = os.path.dirname(sublime.packages_path())
        sublime_user_path = os.path.join(sublime_path, "Packages", "User")
        plugin_data_path = os.path.join(sublime_user_path, "Competitive Programming Lite")
        plugin_path = plugin_data_path

        project_window = sublime.active_window()

        # Handling Input Values
        with open(os.path.join(plugin_path, "templates/templates.json"), "r") as f:
            language_templates = json.load(f)
        templates = {i: "{0} ({1})".format(j[0], j[1]) for i, j in language_templates.items()}
        if template in templates.values():
            template = list(templates.keys())[list(templates.values()).index(template)]
        else:
            sublime.message_dialog("Please add a template first.")
            return

        # Opening Template File
        template_name = language_templates[template][0]
        language_extension = language_templates[template][2]
        project_window.run_command("open_file", {"file": os.path.join(plugin_path, "templates/{0}.{1}".format(template_name, language_extension))})

    # Getting Template Input
    def input(self, args):
        if "template" not in args:
            return TemplateInputHandlerND()


# Command for Deleting a Template
class CpDeleteCommand(sublime_plugin.TextCommand):
    # Default run Command
    def run(self, edit, template):
        plugin_init()

        sublime_path = os.path.dirname(sublime.packages_path())
        sublime_user_path = os.path.join(sublime_path, "Packages", "User")
        plugin_data_path = os.path.join(sublime_user_path, "Competitive Programming Lite")
        plugin_path = plugin_data_path

        # Handling Input Values
        with open(os.path.join(plugin_path, "templates/templates.json"), "r") as f:
            language_templates = json.load(f)
        templates = {i: "{0} ({1})".format(j[0], j[1]) for i, j in language_templates.items()}
        if template in templates.values():
            template = list(templates.keys())[list(templates.values()).index(template)]
        else:
            sublime.message_dialog("Please add a template first.")
            return

        # Confirmation
        if not sublime.ok_cancel_dialog("Are you sure you want to delete {0} template?".format(templates[template]), "Yes"):
            return

        # Removing Template File
        with open(os.path.join(plugin_path, "templates/templates.json"), "r") as f:
            templates_data = json.load(f)
        template_name = templates_data[template][0]
        language_extension = templates_data[template][2]
        del templates_data[template]
        with open(os.path.join(plugin_path, "templates/templates.json"), "w") as f:
            f.write(json.dumps(templates_data, indent=4))

        # Deleting Template File
        os.remove(os.path.join(plugin_path, "templates/{0}.{1}".format(template_name, language_extension)))

    # Getting Template Input
    def input(self, args):
        if "template" not in args:
            return TemplateInputHandlerND()


# Command for Setting Key Bindings
class CpKeyBindingsCommand(sublime_plugin.TextCommand):
    # Default run Command
    def run(self, edit):
        plugin_init()

        project_window = sublime.active_window()
        project_window.run_command("edit_settings", {
            "base_file": "${packages}/Competitive Programming Lite/sublime/Default ($platform).sublime-keymap",
            "user_file": "${packages}/User/Competitive Programming Lite/sublime/Default ($platform).sublime-keymap",
            "default": "[\n\t$0\n]\n"
        })


# Command for Opening Help Page
class CpHelpCommand(sublime_plugin.TextCommand):
    # Default run Command
    def run(self, edit):
        project_window = sublime.active_window()
        project_window.run_command("open_url", {"url": "https://github.com/JameelKaisar/Competitive-Programming-Lite"})


# Handler for Getting Total Questions Input
class QuestionsInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "questions"
    def placeholder(self):
        return "Enter Number of Questions"
    def preview(self, questions):
        if questions.isdigit() and int(questions):
            return "Questions: {0}".format(questions)
        else:
            return "Default: 6"


# Handler for Getting Question Number Input
class QuestionInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "question"
    def placeholder(self):
        return "Enter Question Number"
    def preview(self, question):
        if question.isdigit() and int(question):
            return "Question: {0}".format(question)
        else:
            return "Default: 1"


# Handler for Getting Template Input
class TemplateInputHandler(sublime_plugin.ListInputHandler):
    def __init__(self):
        plugin_init()

        sublime_path = os.path.dirname(sublime.packages_path())
        sublime_user_path = os.path.join(sublime_path, "Packages", "User")
        plugin_data_path = os.path.join(sublime_user_path, "Competitive Programming Lite")
        plugin_path = plugin_data_path

        with open(os.path.join(plugin_path, "templates/templates.json"), "r") as f:
            language_templates = json.load(f)
        self.templates = {i: "{0} ({1})".format(j[0], j[1]) for i, j in language_templates.items()}
    def name(self):
        return "template"
    def placeholder(self):
        return "Select Template"
    def list_items(self):
        return [x for x in self.templates.values()]
    def preview(self, template):
        return "Selected: {0}".format(template)


# Handler for Getting Template Input (No Default)
class TemplateInputHandlerND(sublime_plugin.ListInputHandler):
    def __init__(self):
        plugin_init()

        sublime_path = os.path.dirname(sublime.packages_path())
        sublime_user_path = os.path.join(sublime_path, "Packages", "User")
        plugin_data_path = os.path.join(sublime_user_path, "Competitive Programming Lite")
        plugin_path = plugin_data_path

        with open(os.path.join(plugin_path, "templates/templates.json"), "r") as f:
            language_templates = json.load(f)
        self.templates = {i: "{0} ({1})".format(j[0], j[1]) for i, j in language_templates.items() if j[0] != "Default"}
    def name(self):
        return "template"
    def placeholder(self):
        return "Select Template"
    def list_items(self):
        return [x for x in self.templates.values()]
    def preview(self, template):
        return "Selected: {0}".format(template)


# Handler for Getting Language Input
class LanguageInputHandler(sublime_plugin.ListInputHandler):
    def __init__(self):
        plugin_init()

        sublime_path = os.path.dirname(sublime.packages_path())
        sublime_user_path = os.path.join(sublime_path, "Packages", "User")
        plugin_data_path = os.path.join(sublime_user_path, "Competitive Programming Lite")
        plugin_path = plugin_data_path

        with open(os.path.join(plugin_path, "languages/languages.json"), "r") as f:
            languages = json.load(f)
        self.languages = {i: j[0] for i, j in languages.items()}
    def name(self):
        return "language"
    def placeholder(self):
        return "Select Language"
    def list_items(self):
        return [x for x in self.languages.values()]
    def preview(self, language):
        return "Selected: {0}".format(language)


# Handler for Getting Name Input
class NameInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "name"
    def placeholder(self):
        return "Enter Name of Template"
    def preview(self, name):
        if name == "":
            return "Enter Name of Template"
        elif all(c.isalnum() or c == ' ' for c in name) and not name.isspace():
            return "Name: {0}".format(name)
        else:
            return "Invalid Name"
