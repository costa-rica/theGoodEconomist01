from flask import Blueprint
from flask import render_template, url_for, redirect, flash, request, abort, session,\
    Response, current_app, send_from_directory, after_this_request
# from datetime import datetime
from datetime import timedelta
from datetime import date
import datetime
import os
from folioApp.datatools.utils import allowedFileUtil, uploadToDfUtil, textToDfUtil, \
    getStsUtil, toExcelUtility, makeDfUtil, seriesIdTitleListIndustry, priceIndicesToDf, \
    formatSeriesIdListUtil, buildMetaDfUtil, makeExcelObj_priceindices, \
    checkStatusUtility, annualizeDf, seriesIdTitleListCommodity, \
    searchQueryCageToDf, cageExcelObjUtil, makeSearchExactDict, \
    updateDbWithApi
import pandas as pd
import numpy as np
from folioApp import db
from folioApp.models import Industrynames,Industryvalues
from folioApp.modelsCage import Cagecompanies

datatools = Blueprint('datatools', __name__)

@datatools.route("/dataTools")
def dataTools():
    return render_template('dataTools.html')


@datatools.route("/security", methods=['POST','GET'])
@datatools.route("/getSTS", methods=['POST','GET'])
def getSTS():
    siteTitle = "Get STS Codes"
    today = date.today().strftime("%m/%d/%Y")
    
    if request.args.get('goToPriceIndices'):
        return redirect(url_for('datatools.priceIndices', goTo=request.args.get('goToPriceIndices')))
    
    if request.method=="POST":
        formDict = request.form.to_dict()
        filesDict = request.files.to_dict()
        
        uploadFilename = filesDict.get('uploadedFile').filename
        uploadedText = formDict.get('textareaEntry')
        
        #check file data upload type
        #make df from data upload
        if uploadFilename:
            uploadedFile = request.files['uploadedFile']
            if '.' in uploadFilename and uploadFilename.rsplit('.', 1)[1].lower() in ['xlsx', 'csv']:
                uploadDf=uploadToDfUtil(uploadFilename, uploadedFile)
            else:
                flash(f'File not accepted ', 'warning')
                return redirect(url_for('datatools.getSTS'))
        elif uploadedText:
            uploadDf=textToDfUtil(uploadedText)
        else:
            flash(f'No web addresses provided. Enter url in text box or upload spreadsheet', 'warning')
            return redirect(url_for('datatools.getSTS'))
        
        makeDfUtil(uploadDf)
            
        if formDict.get('button') == 'makeTable':
            stsTable = pd.read_excel(os.path.join(current_app.config['GET_STS_FILES'], 'STS Codes Report.xlsx'))
            stsTable['Date']=stsTable['Date'].dt.date
            stsTableColumns = stsTable.columns
            stsTable=stsTable.to_dict('records')
            return render_template("getSts.html", siteTitle = siteTitle,stsTable=stsTable, stsTableColumns=stsTableColumns, len=len)       

        elif formDict.get('button') == 'downloadTable':
            return send_from_directory(os.path.join(current_app.root_path, 'static','getSts'),'STS Codes Report.xlsx', as_attachment=True)
            
        # return render_template("getSts.html")
    return render_template("getSts.html", siteTitle = siteTitle)

@datatools.route('/blsIndustry',methods=['POST','GET'])
def blsIndustry():
    #Delete download file if exists
    if os.path.exists(os.path.join(current_app.static_folder, 'blsIndustry','blsIndustryPPI.xlsx')):
        os.remove(os.path.join(current_app.static_folder, 'blsIndustry','blsIndustryPPI.xlsx'))
    siteTitle = "BLS Industry Producer Price Index (PPI)"
    session['textareaEntry'] = request.args.get('textareaEntry_new')
    cs0=request.args.get('cs0')
    cs1=request.args.get('cs1')
    cs2=request.args.get('cs2')
    cs3=request.args.get('cs3')
    cs4=request.args.get('cs4')
    cs5=request.args.get('cs5')
    cs6=request.args.get('cs6')
    cs7=request.args.get('cs7')
    cs8=request.args.get('cs8')
    cs9=request.args.get('cs9')
    cs10=request.args.get('cs10')
    cs11=request.args.get('cs11')
    cs12=request.args.get('cs12')
    cs13=request.args.get('cs13')
    colNames=['series_id','series_title']
    indexSeriesIdTitleList=seriesIdTitleListIndustry()

    if request.method=="POST":
        formDict = request.form.to_dict()
        textareaEntry_new=formDict.get('textareaEntry')
        addSeries_id=formDict.get('addSeries_id')
        periodicity = formDict.get('periodicty')
        print('formDict:::',formDict)
        

        if addSeries_id:
            csUtil = checkStatusUtility(formDict)
            if textareaEntry_new != None and textareaEntry_new != "":
                textareaEntry_new = textareaEntry_new + ',\n' + addSeries_id
            else:
                textareaEntry_new = addSeries_id 
            return redirect(url_for('datatools.blsIndustry', textareaEntry_new=textareaEntry_new, cs0=csUtil[0],
                cs1=csUtil[1],cs2=csUtil[2],cs3=csUtil[3],cs4=csUtil[4],cs5=csUtil[5],cs6=csUtil[6],cs7=csUtil[7],
                cs8=csUtil[8],cs9=csUtil[9],cs10=csUtil[10], cs11=csUtil[11],cs12=csUtil[12],cs13=csUtil[13]))

        elif formDict.get('downloadButton') and textareaEntry_new != '':
            seriesIdList=session['textareaEntry'].replace('\r\n','')
            #make seriesId for db/api check and indexValuesDf
            seriesIdListClean=formatSeriesIdListUtil(seriesIdList)
            print('Series Requested: ',seriesIdListClean)
            
            updateDbWithApi(seriesIdListClean, 'industryvalues')#<---checks db for requested data not current
            #if any requested data is not of a month 2 months and 13 days from the current date then api call
            
            indexValuesDf=priceIndicesToDf(seriesIdListClean,'Industry')

            #make list for meta data
            metaDataItemsList=[i[:-8] for i in formDict.keys() if 'Checkbox' in i]

            #use list to make metadata indexValuesDf
            metaDf = buildMetaDfUtil(seriesIdListClean, metaDataItemsList, 'Industry')

            #create ExcelWriter object with date formatted, col heading formatted and values centered
            filePathAndName=os.path.join(current_app.static_folder, 'blsIndustry','blsIndustryPPI.xlsx')
            sheetName='Indices'

            excelObj=makeExcelObj_priceindices(filePathAndName,metaDf,indexValuesDf,seriesIdListClean,
                metaDataItemsList,sheetName, periodicity)
            excelObj.close()
            return send_from_directory(os.path.join(current_app.static_folder, 'blsIndustry'),'blsIndustryPPI.xlsx', as_attachment=True)

            
        elif formDict.get('clearButton'):
            if os.path.exists(os.path.join(current_app.static_folder, 'blsIndustry','blsIndustryPPI.xlsx')):
              os.remove(os.path.join(current_app.static_folder, 'blsIndustry','blsIndustryPPI.xlsx'))

            return redirect(url_for('datatools.blsIndustry', cs11="checked"))
        else:
            flash(f'No indices requested', 'warning')
            return redirect(url_for('datatools.blsIndustry'))
            
    return render_template('blsIndustry.html', siteTitle=siteTitle, indexSeriesIdTitleList=indexSeriesIdTitleList,
    colNames=colNames, len=len, str=str, textareaEntry=session['textareaEntry'], cs0=cs0,
                cs1=cs1,cs2=cs2,cs3=cs3,cs4=cs4,cs5=cs5,cs6=cs6,cs7=cs7,cs8=cs8,cs9=cs9,cs10=cs10,cs11=cs11,
                cs12=cs12,cs13=cs13)


@datatools.route('/blsCommodity',methods=['POST','GET'])
def blsCommodity():
    #Delete download file if exists
    if os.path.exists(os.path.join(current_app.static_folder, 'blsCommodity','blsCommodityPPI.xlsx')):
        os.remove(os.path.join(current_app.static_folder, 'blsCommodity','blsCommodityPPI.xlsx'))
    siteTitle='BLS Commodity Producer Price Index (PPI)'
    session['textareaEntry'] = request.args.get('textareaEntry_new')
    cs0=request.args.get('cs0')
    cs1=request.args.get('cs1')
    cs2=request.args.get('cs2')
    cs3=request.args.get('cs3')
    cs4=request.args.get('cs4')
    cs5=request.args.get('cs5')
    cs6=request.args.get('cs6')
    cs7=request.args.get('cs7')
    cs8=request.args.get('cs8')
    cs9=request.args.get('cs9')
    cs10=request.args.get('cs10')
    cs11=request.args.get('cs11')
    cs12=request.args.get('cs12')
    cs13=request.args.get('cs13')
    colNames=['series_id','series_title']
    indexSeriesIdTitleList=seriesIdTitleListCommodity()
    
    if request.method=="POST":
        formDict = request.form.to_dict()
        textareaEntry_new=formDict.get('textareaEntry')
        addSeries_id=formDict.get('addSeries_id')
        periodicity = formDict.get('periodicty')

        if addSeries_id:
            csUtil = checkStatusUtility(formDict)
            if textareaEntry_new != None and textareaEntry_new != "":
                textareaEntry_new = textareaEntry_new + ',\n' + addSeries_id
            else:
                textareaEntry_new = addSeries_id 
            return redirect(url_for('datatools.blsCommodity', textareaEntry_new=textareaEntry_new, cs0=csUtil[0],
                cs1=csUtil[1],cs2=csUtil[2],cs3=csUtil[3],cs4=csUtil[4],cs5=csUtil[5],cs6=csUtil[6],cs7=csUtil[7],
                cs8=csUtil[8],cs9=csUtil[9],cs10=csUtil[10], cs11=csUtil[11],cs12=csUtil[12],cs13=csUtil[13]))

        elif formDict.get('downloadButton') and textareaEntry_new != '':
            seriesIdList=session['textareaEntry'].replace('\r\n','')
            #make seriesId for indexValuesDf
            seriesIdListClean=formatSeriesIdListUtil(seriesIdList)
            print(seriesIdListClean)
            indexValuesDf=priceIndicesToDf(seriesIdListClean,'Commodity')

            updateDbWithApi(seriesIdListClean, 'commodityvalues')#<---checks db for requested data not current
            #if any requested data is not of a month 2 months and 13 days from the current date then api call
            
            indexValuesDf=priceIndicesToDf(seriesIdListClean,'Commodity')

            #make list for meta data
            metaDataItemsList=[i[:-8] for i in formDict.keys() if 'Checkbox' in i]
            print('metaDataItemsList:::',metaDataItemsList)

            #use list to make metadata indexValuesDf
            metaDf = buildMetaDfUtil(seriesIdListClean, metaDataItemsList, 'Commodity')

            #create ExcelWriter object with date formatted, col heading formatted and values centered
            filePathAndName=os.path.join(current_app.static_folder, 'blsCommodity','blsCommodityPPI.xlsx')
            sheetName='Indices'
            #if annualize
            excelObj=makeExcelObj_priceindices(filePathAndName,metaDf,indexValuesDf,seriesIdListClean,
                metaDataItemsList,sheetName, periodicity)
            excelObj.close()
            return send_from_directory(os.path.join(current_app.static_folder, 'blsCommodity'),'blsCommodityPPI.xlsx', as_attachment=True)

            
        elif formDict.get('clearButton'):
            if os.path.exists(os.path.join(current_app.static_folder, 'blsCommodity','blsCommodityPPI.xlsx')):
              os.remove(os.path.join(current_app.static_folder, 'blsCommodity','blsCommodityPPI.xlsx'))

            return redirect(url_for('datatools.blsCommodity', cs11="checked"))
        else:
            flash(f'No indices requested', 'warning')
            return redirect(url_for('datatools.blsCommodity'))
            
            
    return render_template('blsCommodity.html', siteTitle=siteTitle, indexSeriesIdTitleList=indexSeriesIdTitleList,
        colNames=colNames, len=len, str=str, textareaEntry=session['textareaEntry'], cs0=cs0,
        cs1=cs1,cs2=cs2,cs3=cs3,cs4=cs4,cs5=cs5,cs6=cs6,cs7=cs7,cs8=cs8,cs9=cs9,cs10=cs10,cs11=cs11,
        cs12=cs12,cs13=cs13)



@datatools.route('/cageCodeSearch',methods=['POST','GET'])
def cageCodeSearch():
    #Delete download file if exists
    # if os.path.exists(os.path.join(current_app.static_folder, 'blsCommodity','blsCommodityPPI.xlsx')):
        # os.remove(os.path.join(current_app.static_folder, 'blsCommodity','blsCommodityPPI.xlsx'))
    siteTitle='CAGE Code Lookup'
    searchDictClean={'companyName':'Company Name', 'companyNameSub':'Company Name (Subsidiary)','cageCode': 'CAGE Code',
        'address': 'Address', 'city': 'City', 'state': 'State'}
    if request.method=="POST":
        formDict = request.form.to_dict()
        if formDict.get('clearButton'):
            return redirect(url_for('datatools.cageCodeSearch'))

        searchStringDict,exactDict = makeSearchExactDict(formDict)
        #re-Key searchStringDict for webpage
        searchDictClean={'companyName':'Company Name', 'companyNameSub':'Company Name (Subsidiary)','cageCode': 'CAGE Code',
            'address': 'Address', 'city': 'City', 'state': 'State'}
        searchStringDict={searchDictClean[i]:j for i,j in searchStringDict.items()}
        exactDict={searchDictClean[i]:j for i,j in exactDict.items()}
        
        count=0
        for i in searchStringDict.values():
            count=count + len(i)
        if count<2:
            flash(f'Query too broad. Must enter at least two search characters to narrow search.', 'warning')
            return redirect(url_for('datatools.cageCodeSearch'))

        df=searchQueryCageToDf(formDict)
        resultsCount = len(df)
        if resultsCount>10000:
            flash(f'Query beyond 10,000 row limit. Must enter more search criteria to narrow search.', 'warning')
            return redirect(url_for('datatools.cageCodeSearch'))
        if formDict.get('searchCage')=='search':
            columnNames = df.columns
            dfResults = df.to_dict('records')
            print('searchStringDict:::',searchStringDict)
            
            return render_template('cageCodeSearch.html', siteTitle=siteTitle, columnNames=columnNames, dfResults=dfResults,
                len=len, searchStringDict=searchStringDict, exactDict=exactDict, searchDictClean=searchDictClean,
                resultsCount='{:,}'.format(resultsCount))
        if formDict.get('searchCage')=='download':
            filePathAndName=os.path.join(current_app.static_folder, 'cageSearch','CAGE_SearchResults.xlsx')
            excelObj=cageExcelObjUtil(filePathAndName,df)
            excelObj.close()
            return send_from_directory(os.path.join(current_app.static_folder, 'cageSearch'),'CAGE_SearchResults.xlsx', as_attachment=True)
    return render_template('cageCodeSearch.html', siteTitle=siteTitle, searchDictClean=searchDictClean)



@datatools.route('/downloadPage',methods=['POST','GET'])
def downloadPage():
    #find a way to clear textarea after clicking download
    # @after_this_request
    # def sendFile(response):
        # return send_from_directory(os.path.join(current_app.static_folder, 'priceindices'),'Price Indices.xlsx', as_attachment=True)
    return render_template('downloadPage.html')