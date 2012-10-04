import sublime, sublime_plugin
import subprocess, threading

class CompileOnSave(sublime_plugin.EventListener):
    def on_post_save(self, view):
        settings = sublime.load_settings('recess.sublime-settings')
        if settings.get('enabled', False):
            if view.file_name()[-5:] == ".less":
                view.run_command("compile_less_with_recess")

class CompileLessWithRecessCommand(sublime_plugin.TextCommand):
    def run(self, text):
        project_folder = sublime.active_window().folders()[0]
        settings = sublime.load_settings('recess.sublime-settings')
        targets = settings.get("targets")
        errors = False
        for target in targets:
            cmd = ["recess", "--compile", "--compress", "%s/%s" % (project_folder, target['less'])]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            result = p.communicate()[0]
            if result == "":
                errors = True
            else:
                print("Compiling less file %s/%s" % (project_folder, target['less']))
                print("Writing compiled css: %s/%s" % (project_folder, target['css']))
                with open("%s/%s" % (project_folder, target['css']), 'wt') as f:
                    f.write(result)
        if errors:
            sublime.error_message("Couldn't compile one or more .less files, parse error? Try running recess manually.")
