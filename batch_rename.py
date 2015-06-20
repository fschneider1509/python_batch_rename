#!/usr/bin/env python
import sys
import glob
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# batch_rename.py
# Rename a huge amount of files in a given folder with a given file ending.
# Author: Fabian Schneider
# eMail: fabian(at)fabianschneider.org
# GitHub: fschneider1509.github.com
# Blog: fschneider1509.github.io
# License: GPL2
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DirectoryReader( object ):
	"Read a directory"
	def __init__(self, file_path, pattern ):
		self._file_path = file_path
		self._pattern = pattern
		self._files = []

	def readDirectory( self ):
		# Read the given directory
		file_pattern = self._file_path + self._pattern
		self._files = glob.glob( file_pattern )

	@property
	def files( self ):
	    return self._files

class MassFileRenamer( object ):
	"Rename a bunch of files"
	def __init__( self, file_path, file_list, prefix, counter ):
		self._file_list = file_list
		self._prefix = prefix
		self._file_path = file_path
		self._cnt_files = len( self._file_list )
		self._cnt_len = len( str( self._cnt_files ) )	
		self._counter = counter	

	def renameFiles( self ):
		cntr = self._counter
		new_file_name = None
		# Rename all files that are contained in the file list
		for f in self._file_list:
			cntr = cntr + 1
			new_file_name = self._buildNewFileName( f, cntr )
			print "Old: " + f
			print "New: " + new_file_name
			try:
				os.rename( f, new_file_name )
			except:
				print "Error while renaming file: ", sys.exec_info()[0]


	def _buildNewFileName( self, old_file_name, counter ):
		# Build the new file name
		new_file_name = None
		str_counter = str( counter )
		file_type = self._getFileType( old_file_name )
		new_file_name = self._file_path + self._prefix 
		new_file_name = self._appendLeadingZeros( new_file_name, counter )
		new_file_name = new_file_name + str_counter + file_type
		return new_file_name

	def _appendLeadingZeros( self, new_file_name, counter ):
		diff = 0
		len_counter = len( str( counter ) )
		ret_file_name = new_file_name

		# Set the leading zeros for the file name
		if( len_counter < self._cnt_len ):
			diff = self._cnt_len - len_counter
			for i in xrange( diff + 1 ):
				ret_file_name = ret_file_name + "0"
		else:
			ret_file_name = ret_file_name + "0"

		return ret_file_name

	def _getFileType( self, old_file_name ):
		return old_file_name[ old_file_name.rfind( "." ): ]


cnt_args = len( sys.argv )

if( cnt_args < 4 or cnt_args > 5 ):
	# Print usage of the program
	print "Missing argument!"
	print ""
	print "Usage: batch_rename.py $PATH_TO_FOLDER_WITH_FILES $NEW_NAME $FILE_EXTENSION $COUNTER"
	print "Example:"
	print "batch_rename.py /Users/fabi/Desktop/Holiday_Pictures/ Holiday_ *.JPG 100"
else:
	# Read the given directory
	dirReader = DirectoryReader( sys.argv[1], sys.argv[3] )
	dirReader.readDirectory( )

	# If the counter is missing, the number for the file names
	# starts with 1
	if( cnt_args == 4 ):
		counter = 0
	else:
		counter = sys.argv[4]
		counter = int( counter ) - 1

	# Rename all the found files
	massRenamer = MassFileRenamer( sys.argv[1], dirReader.files, sys.argv[2], counter )
	massRenamer.renameFiles()

# ToDo:
# - Kopfzeile
# - GitHub Folder