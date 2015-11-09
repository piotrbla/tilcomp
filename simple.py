#!/usr/bin/env python
""" Usage: call with <filename> <typename>
"""

import sys
import clang.cindex


def verbose(*args, **kwargs):
    """filter predicate for show_ast: show all"""
    return True


def no_system_includes(cursor, level):
    """filter predicate for show_ast: filter out verbose stuff from system include files"""
    return (level!= 1) or \
           (cursor.location.file is not None and not cursor.location.file.name.startswith('/usr/include'))


# A function show(level, *args) would have been simpler but less fun
# and you'd need a separate parameter for the AST walkers if you want it to be exchangeable.
class Level(int):
    """represent currently visited level of a tree"""
    def show(self, *args):
        """pretty print an indented line"""
        print '\t'*self + ' '.join(map(str, args))

    def __add__(self, inc):
        """increase level"""
        return Level(super(Level, self).__add__(inc))


def is_valid_type(t):
    """used to check if a cursor has a type"""
    return t.kind != clang.cindex.TypeKind.INVALID


def qualifiers(t):
    """set of qualifiers of a type"""
    q = set()
    if t.is_const_qualified():
        q.add('const')
    if t.is_volatile_qualified():
        q.add('volatile')
    if t.is_restrict_qualified():
        q.add('restrict')
    return q


def show_type(t, level, title):
    """pretty print type AST"""
    level.show(title, str(t.kind), ' '.join(qualifiers(t)))
    if is_valid_type(t.get_pointee()):
        show_type(t.get_pointee(), level+1, 'points to:')


def show_ast(cursor, filter_predicate=verbose, level=Level()):
    """pretty print cursor AST"""
    if filter_predicate(cursor, level):
        level.show(cursor.kind, cursor.spelling, cursor.displayname, cursor.location)
        if is_valid_type(cursor.type):
            show_type(cursor.type, level+1, 'type:')
            show_type(cursor.type.get_canonical(), level+1, 'canonical type:')
        for c in cursor.get_children():
            show_ast(c, filter_predicate, level+1)


def find_type_refs(node, typename):
    """ Find all references to the type named 'typename'
    """
    if node.kind.is_reference():
        node_kind = node.kind
        if node_kind == clang.cindex.CursorKind.TYPE_REF:
            print "TYPE_REF"
        # ref_node = clang.cindex.Cursor(node)#Cursor_ref(node)
        # if ref_node.spelling == typename:
        #     print 'Found %s [line=%s, col=%s]' % (
        #         typename, node.location.line, node.location.column)
    # Recurse for children of this node
    for c in node.get_children():
        find_type_refs(c, typename)


def show_only_for_loops(cursor, filter_predicate=verbose, level=Level(), is_for=0):
    """pretty print only for loops from AST"""
    if filter_predicate(cursor, level):
        if cursor.kind == clang.cindex.CursorKind.FOR_STMT:
            is_for = 1
        if is_for:
            level.show(cursor.kind, cursor.spelling, cursor.displayname, cursor.location)
            if is_valid_type(cursor.type):
                show_type(cursor.type, level+1, 'type:')
                show_type(cursor.type.get_canonical(), level+1, 'canonical type:')
        if is_for:
            if cursor.kind == clang.cindex.CursorKind.FOR_STMT or cursor.kind == clang.cindex.CursorKind.COMPOUND_STMT:
                for e in cursor.get_tokens():
                    print 'level: ', level, e.spelling

        for c in cursor.get_children():
            show_only_for_loops(c, filter_predicate, level+1, is_for)


def show_translation_unit(cursor):
                for e in cursor.get_tokens():
                    print e.spelling


def find_and_print_1st_level_for_loops(cursor, filter_predicate=verbose, level=Level(), for_nesting_level=0):
    if filter_predicate(cursor, level):
        if cursor.kind == clang.cindex.CursorKind.FOR_STMT:
            for_nesting_level += 1
        # if for_nesting_level:
        #     level.show(cursor.kind, cursor.spelling, cursor.displayname, cursor.location)
        #     if is_valid_type(cursor.type):
        #         show_type(cursor.type, level+1, 'type:')
        #         show_type(cursor.type.get_canonical(), level+1, 'canonical type:')
        if for_nesting_level == 1:
            for e in cursor.get_tokens():
                print 'level: ', level, e.spelling

        for c in cursor.get_children():
            find_and_print_1st_level_for_loops(c, filter_predicate, level+1, for_nesting_level)


index = clang.cindex.Index.create()
translationUnit = index.parse(sys.argv[1])
print 'Translation unit:', translationUnit.spelling
print 'Printing loops:'
# for f in translationUnit.get_includes():
#     print '\t'*f.depth, f.include.name
# show_ast(translationUnit.cursor, no_system_includes)
# show_only_for_loops(translationUnit.cursor, no_system_includes)
# show_translation_unit(translationUnit.cursor)

find_and_print_1st_level_for_loops(translationUnit.cursor, no_system_includes)

# find_typerefs(translationUnit.cursor, sys.argv[2])
