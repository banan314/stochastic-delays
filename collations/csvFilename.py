def createCSVFilename(filePrefix):
    csvFilename = {}
    for ns in ['N=20', 'N=100', 'N=300', 'N=500']:
        tausValue = {}
        for d in [1, 2, 3, 20, 50, 150]:
            tausValue['d='+str(d)] = '../csv/'+ns+'/'+filePrefix+'-taus-d-'+str(d)+'.csv'
        
        dsValue = {}
        for tau in [1, 2, 3, 4,5,6, 20, 50]:
            dsValue['tau='+str(tau)] = '../csv/'+ns + '/' + filePrefix + '-ds-tau-' + str(tau)+'.csv'
        
        csvFilename[ns] = {'ds': dsValue,
                          'taus': tausValue}
    return csvFilename
