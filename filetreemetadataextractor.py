from typing import List
import json

class FiletreeMetadataExtractor:
    #this class processes the Whole-Genome-Sequence (WGS) data file names and extracts some metadata out of it
    def __init__(self,
                 unparsed_data: List[str],
                 output_path:str
                 ):
        self._unparsed_data: List[str] = unparsed_data
        self._output_path: str = output_path
        self._headers: List[str] = None
        print("initialised extractor object")
    def parseRows(self):
        #read the sample header data in form sample-id|data-type
        rowheader = [ row.split('/')[0]+'|'+row.split('/')[1] for row in self._unparsed_data]
        # remove duplicates in the rowheader
        self._headers = list(set(rowheader))
        output_data = []

        #this block generates the desired data as list of python dict
        for headerrow in self._headers:
            lanes = []
            for row in self._unparsed_data:
                try:
                    if row.split('/')[0] + '|' + row.split('/')[1] == headerrow:
                        splittedrow = row.split('/')
                        splittedrowSub = splittedrow[2].split('_')
                        rowMetaDataLane = {
                            "path": row,
                            "lane": int(splittedrowSub[4][1:]),
                            "marker-forward": splittedrowSub[3].split('-')[0],
                            "marker-reverse": splittedrowSub[3].split('-')[1],
                            "barcode": splittedrowSub[0]
                        }
                        lanes.append(rowMetaDataLane)
                except:
                    print("error in decoding the file name:", row)
            sampleMetaData = {
                "case-id": headerrow.split('|')[0].split('-')[0],
                "sample-label": headerrow.split('|')[0].split('-')[1],
                "sample-id":  headerrow.split('|')[0],
                "data-type": headerrow.split('|')[1],
                "lanes": lanes
            }
            #sample must have at least one appropriate lane
            if len(lanes) > 0:
                output_data.append(sampleMetaData)
        #dump the output data as json with pretty print into file
        with open(self._output_path, 'w') as file_handler:
            json.dump(output_data,file_handler,indent=2)
        print("the data is succesfully written into: ", self._output_path)
