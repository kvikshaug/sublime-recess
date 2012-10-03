import sublime, sublime_plugin
import subprocess

class CompileLessWithRecessCommand(sublime_plugin.TextCommand):
    def run(self, text):
        settings = sublime.load_settings('recess.sublime-settings')
        less_file = "%s/%s" % (sublime.active_window().folders()[0], settings.get("lessFile"))
        css_file = "%s/%s" % (sublime.active_window().folders()[0], settings.get("cssFile"))

        cmd = ["recess", "--compile", "--compress", less_file]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        result = p.communicate()[0]
        if result == "":
            sublime.error_message("Couldn't compile .less files, parse error? Try running recess manually on %s" % less_file)
        else:
            print("Compiling less file %s" % less_file)
            print("Writing compiled css: %s" % css_file)
            with open(css_file, 'wt') as f:
                f.write(result)

class LessToCssSave(sublime_plugin.EventListener):
    def on_post_save(self, view):
        settings = sublime.load_settings('recess.sublime-settings')
        if settings.get('enabled', False):
            if view.file_name()[-5:] == ".less":
                view.run_command("compile_less_with_recess")
