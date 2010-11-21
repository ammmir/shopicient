#!/usr/bin/env python
# -*- coding: ascii -*-
##############################################################################
# Copyright (c) 2010, Erik Karulf (erik@karulf.com)
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
##############################################################################
# barcode_type.py
# http://gist.github.com/541851
#
# Change Log:
# 2010-08-10 - Initial implementation, UPS and USPS tracking based off of
#              comments from: http://stackoverflow.com/questions/619977/
##############################################################################

import re

class BarcodeType(object):
    UPS     = 'ups'
    USPS    = 'usps'
    ISBN13  = 'isbn-13'
    UPC     = 'upc'
    
    _REGEX   = {
        re.compile(r'^(1Z?[0-9A-Z]{3}?[0-9A-Z]{3}?[0-9A-Z]{2}?[0-9A-Z]{4}?[0-9A-Z]{3}?[0-9A-Z]|[\dT]\d\d\d?\d\d\d\d?\d\d\d)$'): 'ups',
        re.compile(r'^(E\D{1}\d{9}\D{2}$|9\d{15,21})$'): 'usps',
        re.compile(r'^(\d{13})$'): 'isbn-13',
        re.compile(r'^(\d{12})$'): 'upc',
    }
    
    @staticmethod
    def resolve(code):
        code = re.sub('\s', '', code)
        for regex, barcode_type in BarcodeType._REGEX.items():
            if regex.match(code):
                return barcode_type
        return None
