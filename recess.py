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
        thread = CompilerThread()
        thread.targets = sublime.load_settings('recess.sublime-settings').get("targets")
        thread.project_folder = sublime.active_window().folders()[0]
        thread.start()

class CompilerThread(threading.Thread):
    def run(self):
        sublime.set_timeout(self.status_start, 0)
        errors = False
        for target in self.targets:
            cmd = ["recess", "--compile", "--compress", "%s/%s" % (self.project_folder, target['less'])]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            result = p.communicate()[0]
            if result == "":
                errors = True
            else:
                print("Compiling less file %s/%s" % (self.project_folder, target['less']))
                print("Writing compiled css: %s/%s" % (self.project_folder, target['css']))
                with open("%s/%s" % (self.project_folder, target['css']), 'wt') as f:
                    f.write(result)

        if errors:
            sublime.set_timeout(self.status_end_error, 0)
        else:
            sublime.set_timeout(self.status_end_success, 0)

    def status_start(self):
        sublime.status_message("Compiling .less files...")

    def status_end_success(self):
        sublime.status_message("Saved compiled css from less.")

    def status_end_error(self):
        sublime.error_message("Couldn't compile one or more .less files, parse error? Try running recess manually.")
