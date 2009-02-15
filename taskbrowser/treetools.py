#Different tools used by the TaskBrowser
import gtk
import gobject

######### TreeStore Tools ######################################
#Constant
TASK_MODEL_DDATE_STR = 2

#Returning a tree store to handle the active task
def new_task_ts(dnd_func=None): 
    task_ts        = gtk.TreeStore( gobject.TYPE_PYOBJECT, \
                                    str,                   \
                                    str,                   \
                                    str,                   \
                                    str,                   \
                                    gobject.TYPE_PYOBJECT, \
                                    str)
    #this is our manual drag-n-drop handling
    if dnd_func : 
        task_ts.connect("row-changed",dnd_func,"insert")
        task_ts.connect("row-deleted",dnd_func,None,"delete")
    return task_ts
    
######## Tree View Tools #######################################

def add_column(name, value, icon=False, padding=None) :
    col = gtk.TreeViewColumn()
    col.set_title(name)
    
    if icon:
        render_pixbuf = gtk.CellRendererPixbuf()
        col.pack_start(render_pixbuf, expand=False)
        col.add_attribute(render_pixbuf, 'pixbuf', 2)
        #col.add_attribute(render_pixbuf, "cell_background",1)
        render_pixbuf.set_property("xpad",2)
        
    render_text = gtk.CellRendererText()
    col.pack_start(render_text, expand=True)
    col.set_attributes(render_text, markup=value)
    #col.add_attribute(render_text, "cell_background",1)
    if padding:
        render_text.set_property("ypad",padding)        

    #col.pack_start(renderer)
    col.set_resizable(True)        
    col.set_sort_column_id(value)
    return col