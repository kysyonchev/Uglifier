import    ast;import    io
import os; import random; import  sys; import   tokenize
from   collections import namedtuple   

Tok=namedtuple ('Tok' ,    'type string start end' )   
FRAGMENTS  = ['TODO: ask Gary about the thing'  , 'why is the sky green',   "don't touch this, it is load-bearing"   , 'banana'  ,'???', 'see page 47','this used to be a llama' ,  'temporary (since 2011)',    'works on my machine',  'left as an exercise for the reader',   'the cat did this'   , 'FIXME later'    ,'do not feed after midnight',    'trust me','42','remember to buy milk'    ,   'here be dragons', 'who wrote this??',   'sorry', "it's wednesday somewhere"  ,'spaghetti'   ,  'refactor when the moon is full', 'not sure but it looks important'  , 'ignore previous comment'    ,   'this line intentionally left confusing', 'ask the duck', 'coffee break',  'yes','no'  , 'maybe', 'asdf', 'lorem ipsum dolor sit amet'  , 'I have no idea either',  'definitely not a bug','was here first',  'and then it rained',    'do not read', 'hello?', 'the printer is haunted'   ,   'borrowed from a dream' ]; WORDS =    [  'purple'    ,'elevator'  ,    'tax', 'noodle', 'quantum',    'sock' , 'fridge', 'meeting' ,'raccoon'    , 'carpet'    ,'lamp'   ,'thursday', 'pigeon'   , 'spreadsheet'   , 'umbrella',  'turnip',   'bureaucracy', 'marmalade','tuba',  'cactus'   , 'invoice'    ,    'yodel','gravel'  , 'sandwich'  , 'wizard' , 'moss',  'clipboard' , 'pancake', 'lighthouse', 'dentist',   'trampoline','velvet', 'accordion',   'soup'] 
       
  

SYMBOLS  = ['!!!'    ,   '...'   ,  '???',   '-----',    '= = =', '~~~~'  , 'xxx',  '<<< >>>' ,   '***'    ,'hmm'  , '@#$%'   ];  INDENT_WIDTHS  =   (1, 2,3   , 4    ,5, 6    ,   8)
SKIP ={tokenize   .    NL,   tokenize  .NEWLINE  , tokenize    .COMMENT,  tokenize . INDENT,tokenize.DEDENT, tokenize  . ENDMARKER};  DEFAULT_OPTS =  dict  (   strip_docstrings    =False    , junk_comments   =True ,   messy_spacing=   True, random_indent    =  True , blank_lines=True  , semicolons=True,  bracket_breaks=True   ,   chaos =   0.7  )
       
  
       
def junk_comment    (rng   ):
        r    = rng  .random (  )
        if  r <0.45:
           text =  rng    .  choice(FRAGMENTS    )
        elif   r    < 0.8  :    

       
          text =    ' '.join  (rng.choices   (WORDS   ,   k=   rng.randint(    2, 6 ))   )    
        elif r < 0.9:
                text=rng. choice(SYMBOLS)
        else  :  
              text = f'{rng.choice(WORDS)} {rng.randint(0, 9999)}'
  
       
        return text   .upper( ) if   rng. random   ( ) <0.08 else  text
def strip_docstrings(   tree)  :

       

     for node    in ast. walk    (    tree  ):

    
         if   isinstance( node   ,(ast.Module,ast. FunctionDef, ast.AsyncFunctionDef, ast    .ClassDef)):
                 b  = node    .  body  
  

  
                 if b and  isinstance(b[   0],   ast.Expr    ) and isinstance (  b[0]   .value    ,   ast.Constant)and  isinstance  (   b [0].value.value,str    ):   
    
  
                   node    .   body    =    b  [1:] or  [   ast .Pass(  ) ]
     return tree
def   logical_lines  (code):


  
  """Split clean code into [(depth, [Tok, ...]), ...]; f-strings become one token."""; src    =code .   split('\n'  )
  def cut(a,   b):
          if a[0] ==b[0]:
       
       

                return   src[ a[ 0]   - 1][a   [1    ] :b  [1   ]]
          return '\n'.  join([src    [a  [0 ]    - 1 ][a[    1]: ] ]    +src[ a   [0]  :   b[  0   ]  - 1   ]  +   [src[b[0  ] - 1   ][   :b    [ 1]]    ])
  fs =  getattr( tokenize,'FSTRING_START'  ,-1) 
  fe    = getattr(tokenize , 'FSTRING_END',-    1 )    
  lines , toks    ,   depth ,    fdepth   ,  fstart =  (    []    , [], 0, 0  ,None)  
  for t in  tokenize. generate_tokens(io.   StringIO   (code +'\n' )    . readline):

    if fdepth:
  

            if t.type ==   fs    : 
    
       
    
                 fdepth  +=  1
            elif t .    type == fe   :    

  
                    fdepth -=1  
                    if    fdepth== 0 :
                     toks.   append (  Tok   (tokenize   .   STRING,  cut   (fstart,t.end  ),fstart,  t    .end))
    
            continue    
    if t   .type == fs:
     fdepth, fstart =    (  1   ,t.start)
    elif   t   .  type ==tokenize   .INDENT    :
       
        depth  +=1
  
       
    elif    t .type   ==    tokenize    .DEDENT  :
     depth -=    1

       
  
    elif t    .    type==tokenize.NEWLINE:
          if   toks   :
              lines.   append (  (  depth  ,  toks   ))
          toks    =[]
    elif t .  type    ==  tokenize.ENDMARKER:  
       

            break
    elif  t .type not   in(tokenize.NL   , tokenize.    COMMENT):  
     toks.append (Tok(    t.   type,    t. string   ,t.start  ,   t.end   )  ) 



  return lines   

       
def   _sig    (   text ):
  try:

       
       
     return[   t .string for t in   tokenize . generate_tokens(io   .StringIO   (   text+ '\n').readline ) if  t.    type    not in SKIP]

  

  except (   tokenize    .   TokenError, SyntaxError ):
     return None
def _wordlike(   t ):   
 return    t. type in ( tokenize    . NAME    , tokenize.NUMBER   , tokenize.  STRING    )  
def _join (    toks, o ,   rng, mess)  :  

       
    
   c   =    o ['chaos'];  parts  , bd, prev    =(   [   ] , 0   ,  None  ) 
   for t in toks    :
        if prev is    not None:
                std    =  t. start[1   ] -   prev. end[ 1] if t.start[  0]==prev .end   [    0]  else 1
       

  
                need = 1 if   _wordlike( prev) and  _wordlike    (t) else   0

                gap   =    max  (std    ,   need )
                sep=   None
  


                if mess and  o['messy_spacing']  and    (rng.   random(   ) < 0.1 +0.6  *c):   
    
    

                 gap = max    (   need,rng    .    choice(    (0    ,   0,  1,   2  , 3   ,  4)   ))
                if mess  and   o  ['bracket_breaks'    ]and   (bd >    0 )   and(prev.    type   ==tokenize   .    OP)and (  prev    .string in(','   , '(',  '[' ,'{'  )   )and(rng    .random   ()   <0.1 + 0.4   * c) : 
                        sep= '\n' + ' '    *   rng   .    choice    ((  0    , 1  , 3 , 6  ,  9   ,12   ,17,    23))
  
                        if o['junk_comments'    ] and  rng.random (   )<   0.25:
                            sep= '  # ' +    junk_comment(rng) +  sep   
                parts.   append(sep if sep is not None else    ' ' *    gap   )    

  
  
        parts . append  (    t.string )
        if t.type == tokenize. OP:   
       


            if t.string in '([{'  :
                    bd+=1
            elif   t.string    in    ')]}':
               bd    -=   1  
  

       
        prev  =   t
   return ''    .join  (    parts )


def _messy_line    (   toks  ,o, rng) :
  
    
   clean =    _join(   toks,o, rng, False)



   if not   (o[ 'messy_spacing' ] or   o   [    'bracket_breaks']):
       

       
      return clean


   want = _sig(clean    )

    
   if want  is  None  :  
    
    

    return clean
   for    _ in range  (3):   

    
       
           cand= _join ( toks,o, rng   ,   True    )
       

       
           if _sig   (    cand   )==    want    :
    
             return    cand 

  
       
   return clean


       
def render(lines, o,    rng    )    :
 c=o  [   'chaos']  

 items   = [    ]

 for depth, toks   in lines :   
       text=_messy_line(toks,   o,rng); simple  = toks[0 ].string  != '@' and toks [  - 1    ]. string    !=':'

    
       if  o  [    'semicolons'   ]  and items and   simple and    items [    -1][2   ]   and( items[-   1]    [0] ==   depth) and   (items    [- 1  ]   [   3]<4) and (  rng.random()   < 0.05+ 0.4   * c ):
            items[-1    ]   [1] += ';' + ' ' * rng. choice   (    (0,    1, 1 ,2))    +   text
            items   [  -1  ]  [3 ] += 1
  

       
       else :  
    
  
             items .append   ([depth   , text    ,   simple, 1]   )

  
    
 out   , stack,prev_depth =    (    [], [ 0    ]    ,   0)   
    

 for depth,text   ,   _,    _ in   items   :

       

       if   depth>    prev_depth:
         stack   . append( stack   [-  1 ]  +  (rng.    choice(    INDENT_WIDTHS   )  if o[  'random_indent'   ]else    4))
    
       else:
       
       
         del stack[depth  + 1   :   ]


       prev_depth= depth
       if o   [ 'blank_lines']    and rng.random() < 0.05 + 0.35    *    c    :
        for _  in   range (rng  .randint(  1, 3)   ): 

             out .append    (   ' '    * rng    .  choice(   ( 0, 0 , 0,   2   , 4,   7)  )   )

       if o['junk_comments'] and rng.random ()    < 0.05+ 0.35*   c:
          for   _ in range  (rng  .choice ( (1,   1    ,1,   2, 3    )) )    :


               out.append(' ' *  rng. randint(    0,   14    )    + rng.choice   ((   '# ', '#',    '#  ', '## '))+   junk_comment( rng   )    )
    
       
       line = ' '*   stack  [depth]   +    text    



       if o    ['messy_spacing']   and   rng    .  random   (   ) <  0.05 +    0.3 *  c:
          line +=  ' '    *rng  .randint(1, 4   )   



       if o['junk_comments'] and   rng.random() <0.05 + 0.3 *c   :
          line   +=   rng  . choice(   (' ' , '  ', '   ',  '    '))  +    '# ' +    junk_comment (rng   )
  

       out.append(line)
 return '\n'    .    join( out)
def    uglify_source(source  , opts= None, seed   =None):
    

   """Return (ugly_code, info). Raises SyntaxError if `source` isn't valid Python.""" 
   if not hasattr (ast, 'unparse'   ) :
       raise RuntimeError   ('Python 3.9 or newer is required.'  )  
    
    
   o =dict(   DEFAULT_OPTS    )    
   o.update(   opts   or {   }   ); o['chaos' ] =  max   ( 0.0,  min(1.0 ,float   (o[    'chaos'    ])  ) );rng  =random   .Random(seed )
   removed =sum(  (1 for t in tokenize    .generate_tokens(  io  .StringIO(source  )   .  readline )   if t.    type    == tokenize.   COMMENT)) 
   shebang = source  .    split    ('\n'   ,    1)[0]if  source .startswith   ('#!')  else None
   tree = ast.parse(  source)    
    
  
   if o [ 'strip_docstrings']:

    tree= strip_docstrings    (tree )
       
   clean =   ast.    unparse   ( tree)

  
   ref  = ast.dump(  ast.parse  (  clean)   );  lines=logical_lines(clean  ); safer  =dict(o, semicolons=   False, bracket_breaks=False); safest =dict(safer,  messy_spacing=False ,  random_indent=False   ) 
       
   result , note =  (None, ''   )
   for   attempt  ,    opt in  enumerate((   o,    o    , safer,  safest ) ): 


    cand =  render( lines   ,  opt, rng)

  
    try    :

        if ast.  dump( ast.    parse   (    cand  )) == ref: 
            result =  cand
            note  = ''  if attempt<    2 else 'some messiness skipped to stay safe';break
    


    except ( SyntaxError, ValueError):    

            pass    
   if   result is None :
        result,   note =(clean, 'could not mess this one up safely; comments removed only'   )
   if shebang:   
        result    = shebang    +    '\n' +result
   added=  sum( (1 for   t  in  tokenize.    generate_tokens (io   .StringIO    (   result  +  '\n').readline) if t .  type ==tokenize  . COMMENT    )) -  (1   if    shebang  else 0 )
   return (result + '\n',   {'removed'  :    removed   , 'added':max    (0    , added),'note': note})

       

def    uglify_file(path    , out_path    ,opts=   None    , seed=None):
    with tokenize .open   (   path )  as fh: 
            source =  fh.read(   )

    ugly, info = uglify_source   ( source,  opts  ,    seed)   
    with open( out_path    ,    'w',   encoding    ='utf-8') as fh:
  
        fh.write    (ugly)

    return  info
def  default_out_path( path,folder=None    ):
  


     base, ext = os .path.splitext   (os.path.  basename    (path)); return    os.path.join(   folder or os.  path    .  dirname (os    .    path   .abspath (path ))    , f"{base}_ugly{ext or '.py'}")
       
       
       
def run_gui( )    :
    import  tkinter as  tk
    
    from tkinter  import filedialog,    messagebox, scrolledtext, ttk
    
    class App    (    tk.   Tk):  
       def __init__(   self   )   :
       
               super ().__init__();  self .title('Code Uglifier');self   .  geometry (    '660x720')
               self.minsize(  580,    640); pad= dict  (padx=14, pady  =6)
               ttk    .Label(self,text='Code Uglifier', font  =    ('TkDefaultFont',   18  , 'bold'    )).pack(   anchor='w'    , padx =  14, pady   =(    14, 0))
               ttk.Label(  self   ,  wraplength    =610   ,    text='Pick Python files and get messy-but-working copies. Real comments are removed, nonsense ones are added. Your originals are never changed.') .pack   (   anchor='w',   padx  =14);fbox = ttk   .    LabelFrame  (   self,   text  ='Files',padding=    8  )

               fbox .pack(    fill    =  'x',   **pad)
    
               self .files =  [ ]
               self .    listbox = tk .Listbox    (fbox    , height    =6    , selectmode    =  'extended'   )    
               self.listbox. pack(   side   =    'left', fill=  'both', expand=    True  );sb=    ttk. Scrollbar( fbox, command=self .  listbox.    yview   )
               sb.  pack  ( side='left'  , fill   ='y');self. listbox.config(  yscrollcommand   =sb.set);  btns    =ttk.Frame(  fbox   );  btns. pack (side= 'left', padx   =(   8, 0    )   , fill   =    'y')   
               ttk.Button    (  btns   ,    text    ='Add files...'   ,    command= self.add_files) .pack    (fill    =   'x')
               ttk.    Button(btns    ,  text   =   'Remove selected'  ,    command   =self. remove_selected    )  .   pack(    fill   ='x',   pady=4); ttk   .Button(btns  , text='Clear'  ,    command=self.clear)  .pack(fill=   'x');obox = ttk. LabelFrame    ( self, text='How ugly?'    ,   padding =8   ); obox.pack (fill='x'  ,** pad)
  

               self  .vars  = {};  labels = [('junk_comments','Add meaningless comments')   ,('messy_spacing',  'Messy spacing & trailing spaces' )  , (   'random_indent'  , 'Random indentation widths'    )    ,  (    'blank_lines',    'Random blank lines')  ,   (   'semicolons'    ,'Cram statements together with ;'   )  ,('bracket_breaks', 'Break lines randomly inside ( ) [ ] { }'),   ( 'strip_docstrings'    ,   'Also remove docstrings' )]
    
  
               for i,(  key    ,   text   )   in enumerate(    labels  )   :
                  self    . vars[key]  = tk.BooleanVar  (value   =DEFAULT_OPTS[key    ]   ); ttk  .    Checkbutton( obox   , text= text,  variable =self   .vars[key   ]) .grid(    row   = i //    2,column   =i %2 ,  sticky    ='w', padx  =6,   pady=  2 )  
               srow=    ttk  .Frame(obox)   
               srow.grid(row= 5   , column  =  0, columnspan  =2 , sticky='ew', pady   =   (10, 0   )  ); ttk.Label  (srow,   text ='Messiness'    )  . pack (side    ='left')
               self.chaos =  tk    .DoubleVar(value    =   70 ); self .  chaos_lbl    =  ttk.Label  (srow,   text= '70%'    , width=5)
               ttk.Scale (srow ,from_  =   0 ,    to=100,  variable= self.    chaos   ,  orient =   'horizontal' ,   command=   lambda v: self.chaos_lbl  .config(text=    f'{float(v):.0f}%' )).pack(side='left',   fill='x'    ,  expand=True,   padx    =8 );self.chaos_lbl  .pack(side=    'left')
       


               seedrow =    ttk.    Frame(obox    )    

  

               seedrow .grid(row   =   6, column=    0  ,columnspan= 2    ,  sticky=   'w'    ,  pady=(   8,0 )  ); ttk    .Label    (   seedrow, text='Seed (optional, same seed = same mess):'  ).pack(side=   'left')
    


               self .  seed=    tk    . StringVar(    );ttk. Entry(  seedrow,   textvariable=self. seed    ,    width=12 ).    pack (    side    ='left' , padx =6   )
               sbox =    ttk. LabelFrame(self,   text=   'Save to',  padding=8   );sbox .    pack    (fill   = 'x'    , **pad)
               self.mode  =    tk.  StringVar(value ='beside'); ttk .   Radiobutton(sbox, text   ='Next to each original as  name_ugly.py'  ,variable =    self . mode , value   ='beside' ).  pack    (   anchor=  'w')
               frow=   ttk    . Frame (sbox)
               frow.pack(fill='x')  

    
               ttk   .Radiobutton    ( frow,text  ='A folder:' ,variable    =  self    .mode    ,  value ='folder').  pack  (    side   =  'left'); self .    folder =  tk  .  StringVar    ();ttk .Entry(frow,   textvariable=self. folder  ). pack  ( side   =    'left', fill=    'x'   ,expand    =    True    ,   padx =6 );ttk    .Button (frow, text=  'Browse...'  ,    command    =self. pick_folder). pack (side   =  'left'   )    
  
  
       
               ttk .    Button(  self, text= 'Make it ugly!'  , command =self.run ).    pack (pady    =8,    ipadx=    16,ipady  =4)  
    
               self  .    log   = scrolledtext.  ScrolledText(self  ,  height=9,   state='disabled', wrap=    'word'); self   .log.pack  (fill =   'both',  expand   =True, padx =    14 ,pady =(    0, 14))
       def  say(self , msg) :   
             self  .log.config (state  =    'normal'   )
             self  .log.insert('end',  msg    +  '\n' )

  

             self.log . see(  'end'   )
             self.log  .config   (state  ='disabled')  
             self    .   update_idletasks (   )
       def add_files (self  ):
         for p    in filedialog   .  askopenfilenames( title    = 'Choose Python files',  filetypes= [('Python files', '*.py')  ,    (   'All files', '*.*' )]):
           if p  not in self.files : 
            self   .files   .append(p)
            self    .listbox.insert(   'end' ,p)
       def remove_selected(self)  :  
         for  i in   reversed (self  .listbox.curselection(  )):
                 self. listbox.delete   (i); del self    .files[ i]
       def clear    (self    )   :    
          self. listbox.delete(0  , 'end'    );  self.files=   []  


       def pick_folder(self):
            d =   filedialog  .askdirectory    (title=    'Choose output folder')
  


            if d: 
              self.folder.  set(d); self.   mode    .set    ('folder')
  
       def run(self)    :
            if not self.    files :
  
               messagebox.showinfo('No files' , 'Add at least one Python file first.'   )
               return   
       

            folder = None

            if  self .   mode   .    get  ()    =='folder'    :   
             folder    =   self.    folder   .get    (  ) .strip  ()
             if not  folder or  not  os.path .isdir  (folder    ):  
  
       
                messagebox   . showerror(  'Folder', 'Choose an existing output folder.')

                return
       
            opts    = {k :   v.    get ()  for k  ,  v   in self.vars.items()    }
            opts [  'chaos']=   self.chaos   .get ( )  /100.0   
            seed =self  .seed    .   get    ()  .strip( )or None;  ok = 0
            for  n   , path  in  enumerate   (self .  files)   :


               out =    default_out_path(path,folder)
               if  os. path.abspath( out    ) == os.   path.  abspath(path    ):   



                 self  .say  (f'SKIPPED {path}: output would overwrite the original')  

  
                 continue

    

               try:
  
  

                       info=uglify_file  (   path   ,out, opts,    None if seed is None else   f'{seed}:{n}')
       
       
                       extra    =  f"  ({info['note']})"   if info[   'note']    else ''
                       self    .  say (   f"OK  {os.path.basename(path)} -> {out}\n    removed {info['removed']} comments, added {info['added']} junk ones{extra}") 
                       ok+= 1
               except SyntaxError as e:


                    self  .say ( f'FAILED {path}: not valid Python (line {e.lineno}: {e.msg})')
               except Exception   as e: 
                       self.  say  (   f'FAILED {path}: {e}'  ) 
            self  .say  (f'Done: {ok} of {len(self.files)} file(s) uglified.\n'  )
  

    App(). mainloop    ()
       
       
def  main   ()   :
   if len( sys .argv)   >  1:   
         for   path in sys.   argv   [1 :   ]   :

    
             out    =  default_out_path  (    path  );  info  = uglify_file(path,  out  );  print(   f"{path} -> {out}  ({info['removed']} comments removed, {info['added']} junk added)") 
   else    :  

  

    run_gui()   
if __name__    =='__main__':    



 main() 
