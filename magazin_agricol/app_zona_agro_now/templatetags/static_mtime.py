import os 
from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def static_mtime(path: str) -> str:
   """
   Return url pt. fis static + timestamp (cache bust)
   """
   url: str = static(path)
   full_path: str | None = finders.find(path) # Find a static file with the given path using all enabled finders.
   # url gasit -> cache bust
   if full_path and os.path.exists(full_path):
      mtime = int(os.path.getmtime(full_path))
      # matching will be fine when frontend requests this url 
      return f"{url}?v={mtime}" 
   # url nu e fisier static -> return as-is
   return url
