#!/usr/bin/python

import cgi
from string import Template
import os.path
import sys

templatePrefix = "templates"
gpioPath = "/usr/local/bin/gpio"

templates = {
  "default" : templatePrefix + "/menu.html",
  "header" : templatePrefix + "/header.html",
  "footer" : templatePrefix + "/footer.html",
}

def printContent(content):
  print 'Content-Type: text/html'
  print
  print content

def getTemplate(fields):
  template = ""
  
  if "letter" in fields:
    template = templatePrefix + "/" + fields["letter"].value + '.html'
  else:
    template = templates["default"]
    log("request parameter 'letter' not present, using default template")

  if not os.path.isfile(template) and not os.access(template, os.R_OK):
    template = templates["default"]
    log("template file: " + template + " not accessible, using default template")

  log("rendering template file: " + template)

  return template

def buildContent(template):
  htmlHeader = open(templates["header"]).read()
  htmlFooter = open(templates["footer"]).read()
  htmlBody = open(template).read()

  templateVars = { 'header' : htmlHeader, 'footer' : htmlFooter }

  return Template(htmlBody).substitute(templateVars)

def getPinMapping():
  return {
    "L" : 1,
    "E" : 2,
    "A" : 3,
    "R" : 4,
    "N" : 5,
    }

def disableAllPins():
  log('attempting to disable all pins')
  if hasGpioCapability():
    for key, value in getPinMapping().iteritems():
      writePin(value, 0, 'output')
      log("disabled pin number: " + str(value))

def hasGpioCapability():
  if os.path.isfile(gpioPath) and os.access(gpioPath, os.X_OK):
    return True
  else:
    log("gpio binary located at: " + gpioPath + " not found, not handling.")
    return False

def writePin(pin, value, mode):
  modeCmd = gpioPath + ' mode ' + str(pin) + ' ' + mode
  writeCmd = gpioPath + ' write ' + str(pin) + ' ' + str(value)

  log("attempting to set gpio mode with command: " + modeCmd)
  if hasGpioCapability():
    os.system(modeCmd)

  log("attempting to write to gpio with command: " + writeCmd)
  if hasGpioCapability():
    os.system(writeCmd)

def togglePin(fields):
  pinMapping = getPinMapping()

  disableAllPins()

  if "letter" in fields:
    if fields["letter"].value in pinMapping:
      pin = pinMapping[fields["letter"].value]

      log("attempting to toggle pin: " + str(pin))

      writePin(pin, 1, 'output')
    else:
      log("requested letter: " + fields["letter"].value + " not found in pin map, not toggling any pins")
  else:
    log("request parameter 'letter' not present, not enabling any pins")

def log(msg):
  sys.stderr.write("* " + os.path.basename(__file__) + " - " + msg + "\n")

def handleRequest():
  template = getTemplate(cgi.FieldStorage())
  content = buildContent(template)

  printContent(content)
  togglePin(cgi.FieldStorage())

handleRequest()
