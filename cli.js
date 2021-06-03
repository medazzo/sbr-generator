#!/usr/bin/env node
'use strict';

const path = require('path')
const {spawn} = require('child_process')
const [,, ... args] = process.argv

const child = spawn('python3  -u  '+path.join(__dirname, 'easinGenerator.py'), args, {
  stdio: 'inherit',
  shell: true
});

