# SU_HappyAST
## 题目设计
混淆：轻微魔改了jsobf项目，随机插入了自定义Literal节点，UnaryExpression节点，Identifier节点等，且加大了节点插入深度。

加密：使用了开源js版本的aes和sm3。其中对aes进行了rcon的简单调序，用sm3加密'bingbing'字符串，取结果前16位作为aes的key和iv。



## 题目解析
前面是简单的jsobf混淆，可先使用jsobf的在线网站[https://obf-io.deobfuscate.io/](https://obf-io.deobfuscate.io/)去混淆。

![](https://cdn.nlark.com/yuque/0/2025/png/34607987/1736840734507-c3c7aba1-da7d-4009-bcbd-dca708f5e371.png)

又或是[https://github.com/PerimeterX/restringer](https://github.com/PerimeterX/restringer)等工具。

也可以自己编写AST解析脚本进行去混淆。这里可以学习v_jstools源码来去除大量混淆，去混后几乎和源码差不多，大家在这一块可以自行研究，有很多种解法。

```plain
function pas_ob_encfunc(ast, obsortname){
    var obfuncstr = []
    var obdecname;
    var obsortname;
    function findobsortfunc(path){
        if (!path.getFunctionParent()){
            function get_obsort(path){
                obsortname = path.node.arguments[0].name
                obfuncstr.push('!'+generator(path.node, {minified:true}).code)
                path.stop()
                path.remove()
            }
            path.traverse({CallExpression: get_obsort})
            path.stop()
        }
    }
    function findobsortlist(path){
        if (path.node.id.name == obsortname){
            obfuncstr.push(generator(path.node, {minified:true}).code)
            path.stop()
            path.remove()
        }
    }
    function findobfunc(path){
        var t = path.node.body.body[0]
        if (t && t.type === 'VariableDeclaration'){
            var g = t.declarations[0].init
            if (g && g.type == 'CallExpression' && g.callee.name == obsortname){
                obdecname = path.node.id.name
                obfuncstr.push(generator(path.node, {minified:true}).code)
                path.stop()
                path.remove()
            }
        }
    }
    if (!obsortname){
        traverse(ast, {ExpressionStatement: findobsortfunc})
        traverse(ast, {FunctionDeclaration: findobsortlist})
        traverse(ast, {FunctionDeclaration: findobfunc})
        eval(obfuncstr.join(';'))
    }else{
        function find_outer_def_by_name(ast, v_name){
            function find_ob_root_def_by_name(ast, v_name){
                function get_deep(path){
                    var idx = 0
                    while (path = path.getFunctionParent()){
                        idx++
                    }
                    return idx
                }
                var def_list = []
                function find_root_def(ast, v_name){
                    var is_stop = false
                    traverse(ast, {Identifier: function(path){
                        if (path.node.name == v_name && !is_stop){
                            var temp = path.scope.getBinding(v_name)
                            if (t.isVariableDeclarator(temp.path.node) && t.isIdentifier(temp.path.node.init)){
                                find_root_def(ast, temp.path.node.init.name)
                                is_stop = true
                            }
                            else if(t.isVariableDeclarator(temp.path.node) && t.isFunctionExpression(temp.path.node.init)){
                                def_list.push([get_deep(path), path])
                                is_stop = true
                            }
                            else if (t.isFunctionDeclaration(temp.path.node)){
                                def_list.push([get_deep(path), path])
                                is_stop = true
                            }
                        }
                    }})
                }
                find_root_def(ast, v_name)
                def_list.sort(function(a,b){return a[0]-b[0]})
                var def_first = def_list[0]
                return def_first && def_first[1]+''
            }
            try{
                var name = find_ob_root_def_by_name(ast, v_name)
                if (name){
                    v_name = name
                }else{
                    throw ReferenceError(`"${v_name}" not find.`)
                }
            }catch(e){
                console.log(e)
            }
            function get_deep(path){
                var idx = 0
                while (path = path.getFunctionParent()){
                    idx++
                }
                return idx
            }
            var def_list = []
            function get_env(path){
                return path.findParent(function(e){return t.isFunction(e) || t.isProgram(e)})
            }
            function v_find_func(path){
                if (t.isVariableDeclaration(path.node)){
                    var declarations = path.node.declarations
                    for (var i = 0; i < declarations.length; i++) {
                        if (t.isIdentifier(declarations[i].id) && t.isFunctionExpression(declarations[i].init)){
                            if (declarations[i].id.name == v_name){
                                def_list.push([get_deep(path), path, get_env(path)])
                            }
                        }
                    }
                }
                else if (t.isFunctionDeclaration(path.node)){
                    if (t.isIdentifier(path.node.id) && path.node.id.name == v_name){
                        def_list.push([get_deep(path), path, get_env(path)])
                    }
                }
            }
            traverse(ast, {'VariableDeclaration|FunctionDeclaration': v_find_func})
            def_list.sort(function(a,b){return a[0]-b[0]})
            var first_outer_def = def_list[0]
            var collect_env = []
            var _cache = []
            function get_all_related(_path, _env){
                if (!_path) return 
                if (_cache.indexOf(_path) !== -1){ return }
                _cache.push(_path)
                _path.traverse({Identifier: function(path){
                    function get_stat(tpath){
                        return tpath.findParent(function(e){return get_env(e)==_env&&(t.isDeclaration(e)||t.isStatement(e))})
                    }
                    if (path.node.name != v_name && get_env(path) !== _env){
                        var target = path.scope.getBinding(path.node.name)
                        if (target){
                            if (collect_env.indexOf(target.path) == -1){
                                if (_env === get_env(target.path)){
                                    collect_env.push(get_stat(target.path)||target.path)
                                    var binds = target.path.scope.bindings
                                    var okeys = Object.keys(binds)
                                    for (var idx = 0; idx < okeys.length; idx++) {
                                        for (var idx2 = 0; idx2 < binds[okeys[idx]].referencePaths.length; idx2++) {
                                            var t_name = okeys[idx]
                                            if (t_name !== v_name){
                                                var temp = binds[t_name].referencePaths[idx2]
                                                var temp = temp.findParent(function(e){return get_env(e)==_env&&(t.isDeclaration(e)||t.isStatement(e))})
                                                if (temp && collect_env.indexOf(temp) == -1){
                                                    collect_env.push(temp)
                                                }
                                            }
                                        }
                                    }
                                    get_all_related(target.path, _env)
                                }
                            }
                        }
                    }
                }})
            }
            if (!(first_outer_def && first_outer_def.length)){
                return
            }
            get_all_related(first_outer_def[1], first_outer_def[2])
            var collect_env_sort = []
            first_outer_def[2].traverse({'Declaration|Statement': function(path){
                if (collect_env.indexOf(path) != -1){
                    if (collect_env_sort.indexOf(path) == -1){
                        collect_env_sort.push(path)
                    }
                }
            }})
            var __collect_env_sort = []
            for (var idx = 0; idx < collect_env_sort.length; idx++) {
                var is_decl = t.isFunctionDeclaration(collect_env_sort[idx].node)
                var str = generator(collect_env_sort[idx].node, {minified:true}).code
                if (is_decl){
                    __collect_env_sort[idx] = str
                }else{
                    __collect_env_sort[idx] = `
                    try{
                    ${str}
                    vilame_ob_remove_sign.push(${idx})
                    }catch(e){
                    }
                    `
                }
            }
            function remove_sign(listidx){
                for (var i = 0; i < listidx.length; i++) {
                    try{
                        collect_env_sort[listidx[i]].remove()
                    }catch(e){
                        console.log(e)
                    }
                }
            }
            __collect_env_sort.unshift('var vilame_ob_remove_sign = []')
            return [v_name, __collect_env_sort.join('\n'), remove_sign]
        }
        var [obsortname, evalstr, remove_sign] = find_outer_def_by_name(ast, obsortname)
        console.log(evalstr)
        console.log('--------------- evalstr end ---------------')
        var v_setTimeout = setTimeout
        var v_setInterval = setInterval
        setTimeout = function(a,b){return v_setTimeout(a,0)}
        setInterval = function(a,b){return v_setTimeout(a,0)}
        eval(evalstr)
        setTimeout = v_setTimeout
        setInterval = v_setInterval
        if (typeof vilame_ob_remove_sign != 'undefined'){
            remove_sign(vilame_ob_remove_sign)
        }
        obdecname = obsortname
    }
    var collects = []
    var collect_names = [obdecname]
    var collect_removes = []
    function judge(path){
        return path.node.body.body.length == 1
            && path.node.body.body[0].type == 'ReturnStatement'
            && path.node.body.body[0].argument.type == 'CallExpression'
            && path.node.body.body[0].argument.callee.type == 'Identifier'
            && path.node.id
    }
    function collect_alldecfunc(path){
        if (judge(path)){
            var t = generator(path.node, {minified:true}).code
            if (collects.indexOf(t) == -1){
                collects.push(t)
                collect_names.push(path.node.id.name)
            }
        }
    }
    var collect_removes_var = []
    function collect_alldecvars(path){
        var left = path.node.id
        var right = path.node.init
        if (right && right.type == 'Identifier' && collect_names.indexOf(right.name) != -1){
            var t = 'var ' + generator(path.node, {minified:true}).code
            if (collects.indexOf(t) == -1){
                collects.push(t)
                collect_names.push(left.name)
            }
        }
    }
    traverse(ast, {FunctionDeclaration: collect_alldecfunc})
    traverse(ast, {VariableDeclarator: collect_alldecvars})
    eval(collects.join(';'))
    function parse_values(path){
        var name = path.node.callee.name
        if (path.node.callee && collect_names.indexOf(path.node.callee.name) != -1){
            try{
                path.replaceWith(t.StringLiteral(eval(path+'')))
                collect_removes.push(name)
            }catch(e){}
        }
    }
    traverse(ast, {CallExpression: parse_values})
    function collect_removefunc(path){
        if (judge(path) && collect_removes.indexOf(path.node.id.name) != -1){
            path.remove()
        }
    }
    function collect_removevars(path){
        var left = path.node.id
        var right = path.node.init
        if (right && right.type == 'Identifier' && collect_names.indexOf(right.name) != -1){
            path.remove()
        }
    }
    traverse(ast, {FunctionDeclaration: collect_removefunc})
    traverse(ast, {VariableDeclarator: collect_removevars})
}

function del_sojson_extra(ast){
    function get_root(path){
        var list = [path]
        while (path.parentPath){
            path = path.parentPath
            list.push(path)
        }
        return list[list.length-2]
    }
    function remove_temp1(path, fname){
        var bind = path.scope.getBinding(fname)
        for (var i = 0; i < bind.referencePaths.length; i++) {
            var root = get_root(bind.referencePaths[i])
            root.need_remove = true
            root.traverse({Identifier: function(path){
                var idbind = path.scope.getBinding(path.node.name)
                if (!idbind) return
                get_root(idbind.path).need_remove = true
            }})
        }
    }
    traverse(ast, {
        'FunctionDeclaration|FunctionExpression': function(path){
            if (path.getFunctionParent() == null){
                var ex1 = 0
                var ex2 = 0
                var ex3 = 0
                path.traverse({StringLiteral: function(path){
                    if (path.node.value == 'debugger'){ ex1 = 1 }
                    if (path.node.value == 'action'){ ex2 = 1 }
                    if (path.node.value == 'stateObject'){ ex3 = 1 }
                }})
                if ((ex1 + ex2 + ex3) >= 2){
                    if (path.node.id && path.node.id.name){
                        remove_temp1(path, path.node.id.name)
                    }
                }
                var ex1 = 0
                var ex2 = 0
                var ex3 = 0
                path.traverse({StringLiteral: function(path){
                    if (path.node.value == "\\w+ *\\(\\) *{\\w+ *['|\"].+['|\"];? *}"){ ex1 = 1 }
                    if (path.node.value == "(\\\\[x|u](\\w){2,4})+"){ ex2 = 1 }
                    if (path.node.value == "window"){ ex3 = 1 }
                }})
                if ((ex1 + ex2 + ex3) >= 2){
                    get_root(path).need_remove = true
                    remove_temp1(path, path.parentPath.node.callee.name)
                    remove_temp1(path, path.parentPath.parentPath.node.id.name)
                }
                var ex1 = 0
                var ex2 = 0
                var ex3 = 0
                path.traverse({StringLiteral: function(path){
                    if (path.node.value == "return (function() {}.constructor(\"return this\")( ));"){ ex1 = 1 }
                    if (path.node.value == "debug"){ ex2 = 1 }
                    if (path.node.value == "exception"){ ex3 = 1 }
                }})
                if ((ex1 + ex2 + ex3) >= 2){
                    get_root(path).need_remove = true
                    remove_temp1(path, path.parentPath.node.callee.name)
                    remove_temp1(path, path.parentPath.parentPath.node.id.name)
                }
            }
        }
    })
    traverse(ast, {enter: function(path){
        if (path.need_remove){
            path.remove()
        }
    }})
}
function calcBinary(path){
    var tps = ['StringLiteral', 'BooleanLiteral', 'NumericLiteral']
    var nod = path.node
    function judge(e){
        return (tps.indexOf(e.type) != -1) || (e.type == 'UnaryExpression' && tps.indexOf(e.argument.type) != -1)
    }
    function make_rep(e){
        if (typeof e == 'number'){ return t.NumericLiteral(e) }
        if (typeof e == 'string'){ return t.StringLiteral(e) }
        if (typeof e == 'boolean'){ return t.BooleanLiteral(e) }
        throw Error('unknown type' + typeof e)
    }
    if (judge(nod.left) && judge(nod.right)){
        path.replaceWith(make_rep(eval(path+'')))
    }
}
function del_ob_extra(ast){
    var setinterval_func;
    function find_gar_outfunc(path){
        if (!path.getFunctionParent()){
            function judge(path){
                if ( path.node.callee.type == 'MemberExpression'
                  && path.node.callee.property
                  && path.node.callee.property.type == 'Identifier'
                  && path.node.callee.property.name == 'apply'
                  && path.node.callee.object.type == 'CallExpression'
                  && path.node.callee.object.arguments
                  && path.node.callee.object.arguments[0]
                  && path.node.callee.object.arguments[0].value == 'debugger'
                  && path.node.arguments[0]
                  && path.node.arguments[0].value == 'stateObject'
                    ){
                    var func = path.getFunctionParent().getFunctionParent()
                    setinterval_func = func.node.id.name
                    func.remove()
                }
            }
            path.traverse({CallExpression: judge})
        }
    }}
    function CallToStr(path) {
        var node = path.node;
        if (!t.isObjectExpression(node.init)) 
            return;
        var objPropertiesList = node.init.properties;
        if (objPropertiesList.length == 0)
            return;
        var objName = node.id.name;
        var del_flag = false
        var objkeys = {}
        var objlist = objPropertiesList.map(function(prop){
            var key = prop.key.value
            if(t.isFunctionExpression(prop.value)) {
                var retStmt = prop.value.body.body[0];
                if (typeof retStmt == 'undefined') return;
                if (t.isBinaryExpression(retStmt.argument)) {
                    var repfunc = function(_path, args){
                        if (args.length == 2){
                            _path.replaceWith(t.binaryExpression(retStmt.argument.operator, args[0], args[1]));
                        }
                    }
                }
                else if(t.isLogicalExpression(retStmt.argument)) {
                    var repfunc = function(_path, args){
                        if (args.length == 2){
                            _path.replaceWith(t.logicalExpression(retStmt.argument.operator, args[0], args[1]));
                        }
                    }
                }
                else if(t.isCallExpression(retStmt.argument) && t.isIdentifier(retStmt.argument.callee)) {
                    var repfunc = function(_path, args){
                        _path.replaceWith(t.callExpression(args[0], args.slice(1)))
                    }
                }
                objkeys[key] = repfunc
            }
            else if (t.isStringLiteral(prop.value)){
                var retStmt = prop.value.value;
                objkeys[key] = function(_path){
                    _path.replaceWith(t.stringLiteral(retStmt))
                }
            }
        })
        var fnPath = path.getFunctionParent() || path.scope.path;
        fnPath.traverse({
            CallExpression: function (_path) {
                var _node = _path.node.callee;
                if (!t.isMemberExpression(_path.node.callee))
                    return;
                if (!t.isIdentifier(_node.object) || _node.object.name !== objName)
                    return;
                if (!(t.isStringLiteral(_node.property) || t.isIdentifier(_node.property)))
                    return;
                if (!(objkeys[_node.property.value] || objkeys[_node.property.name]))
                    return;
                var args = _path.node.arguments;
                var func = objkeys[_node.property.value] || objkeys[_node.property.name]
                func(_path, args)
                del_flag = true;
            },
            MemberExpression:function (_path) {
                var _node = _path.node;
                if (!t.isIdentifier(_node.object) || _node.object.name !== objName)
                    return;
                if (!(t.isStringLiteral(_node.property) || t.isIdentifier(_node.property)))
                    return;
                if (!(objkeys[_node.property.value] || objkeys[_node.property.name]))
                    return;
                var func = objkeys[_node.property.value] || objkeys[_node.property.name]
                func(_path)
                del_flag = true;
            }
        })
    
        if (del_flag) {
            path.remove();
        } 
    }
    

function ClearDeadCode(path){
    function clear(path, toggle){
        if (toggle){
            if (path.node.consequent.type == 'BlockStatement'){
                path.replaceWithMultiple(path.node.consequent.body)
            }else{
                path.replaceWith(path.node.consequent)
            }
        }else{
            if (path.node.alternate){
                if (path.node.alternate.type == 'BlockStatement'){
                    path.replaceWithMultiple(path.node.alternate.body)
                }else{
                    path.replaceWith(path.node.alternate)
                }
            }else{
                path.remove()
            }
        }
    }
    var temps = ['StringLiteral', 'NumericLiteral', 'BooleanLiteral']
    if (path.node.test.type === 'BinaryExpression'){
        if (temps.indexOf(path.node.test.left.type) !== -1 && temps.indexOf(path.node.test.right.type) !== -1){
            var left = JSON.stringify(path.node.test.left.value)
            var right = JSON.stringify(path.node.test.right.value)
            clear(path, eval(left + path.node.test.operator + right))
        }
    } else if (temps.indexOf(path.node.test.type) !== -1){
        clear(path, eval(JSON.stringify(path.node.test.value)))
    }
}




function muti_process_obdefusion(jscode){
    var ast = parser.parse(jscode);
    pas_ob_encfunc(ast, ''.trim())
    traverse(ast, {BinaryExpression: {exit: calcBinary}})
    traverse(ast, {VariableDeclarator: {exit: CallToStr},});   
    traverse(ast, {IfStatement: ClearDeadCode});           
  
    del_ob_extra(ast)                                     
    
    var { code } = generator(ast);
    return code;
}

const fs = require('fs');
var jscode = fs.readFileSync("./out.js", {
    encoding: "utf-8"
});
code = muti_process_obdefusion(jscode);
console.log(code);
fs.writeFileSync('./code.js', code, {
    encoding: "utf-8"
})
```

解析完大概只剩下2000行代码（依据反混淆不同写法代码量不同，但不影响分析）。

**从下往上看**，搜索关键数组值，很容易看出是aes源码，进行对比后发现，只改动了rcon的值。对于iv和key，去混淆完可以直接跟逻辑调试，不难发现是50aca6ed2feffa0c

![](https://cdn.nlark.com/yuque/0/2025/png/34607987/1736842179533-e2bb2b02-ad0c-48b6-9fa3-094eab88ec79.png)

自行扣取js版解密脚本即可解密：[https://github.com/ricmoo/aes-js/blob/master/index.js](https://github.com/ricmoo/aes-js/blob/master/index.js)

```plain
_H4PpY_AsT_TTTTTTBing_BinG_Bing}
```

脚本解得后半段flag。

题目和描述没有任何提示，只得继续分析观察AST结构。可尝试遍历不同节点或是用astexplorer细看AST树。其中部分Literal节点和Identifier节点带有部分特征且为无效节点（即no-op节点）。

![](https://cdn.nlark.com/yuque/0/2025/png/34607987/1736841151310-f53b596f-c645-407b-bba8-253fac1b467b.png)

也可直接看代码，解混淆后**从上往下看**，不难发现有许多Bing?Bing类似的Literal节点，UnaryExpression节点或是Identifier节点等。

![](https://cdn.nlark.com/yuque/0/2025/png/34607987/1736841227808-78b613ea-a0d7-487c-a5eb-20f9ae3b4931.png)

这里可用直接使用正则匹配，提取出'Bing?Bing'相关的所有节点。

最后共有八个不同结果，S U C T F { H i

依据flag头进行拼接，flag只有两种可能性：

SUCTF{Hi_H4PpY_AsT_TTTTTTBing_BinG_Bing}

SUCTF{iH_H4PpY_AsT_TTTTTTBing_BinG_Bing}

故最终flag为：

```plain
SUCTF{Hi_H4PpY_AsT_TTTTTTBing_BinG_Bing}
```

