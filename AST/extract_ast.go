package main

import (
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"io/ioutil"
	"strings"
	"os"
	"encoding/json"
)

type functionData struct {
    repoName	string
    Data	[]string
}

func main() {
	
	fmt.Printf("== Start Parsing ==\n")

	repoName := "runc"
	filepath := fmt.Sprintf("{ROOT_DIR}/Source_Code/%s", repoName)

	var wholeFileNames = []string {}
	var wholeFunctions = [] string {}

	GetAllFile(filepath, &wholeFileNames)
	
	// Parse all test files
	for _, filename := range wholeFileNames{
		fmt.Printf("== Parsing File %s ==\n", filename)
		fileFunctions := getAllFunctionsPerFile(filename)
		wholeFunctions = append(wholeFunctions, fileFunctions...)
		fmt.Printf("\n")
	}
	fmt.Printf("allFunction = %v \nFunction number = %d\nSlice cap = %d\n",wholeFunctions,len(wholeFunctions),cap(wholeFunctions))
	
	// duplicate slice
	wholeFunctions = removeRepSlice(wholeFunctions)
	fmt.Printf("allFunction = %v \nFunction number = %d\nSlice cap = %d\n",wholeFunctions,len(wholeFunctions),cap(wholeFunctions))

	// save to json file
	saveToJson(repoName, wholeFunctions)
}

func GetAllFile(pathname string, wholeFileNames *[]string) error {
    rd, err := ioutil.ReadDir(pathname)
    for _, fi := range rd {
        if fi.IsDir() {
			if fi.Name() != "vendor" {
				GetAllFile(pathname + "/" + fi.Name(), wholeFileNames)
			}
            // fmt.Printf("[%s]\n", pathname+"/"+fi.Name())
        } else {
			fullPath := fmt.Sprintf("%s/%s", pathname, fi.Name())
			ok := strings.HasSuffix(fi.Name(), "test.go")
            if ok {
				// fmt.Println(fullPath)
				*wholeFileNames = append(*wholeFileNames, fullPath)
            	}
		}
    }
    return err
}

func getAllFunctionsPerFile(filename string) []string {

	fset := token.NewFileSet()
	node, err := parser.ParseFile(fset, filename, nil, parser.ParseComments)
	if err != nil {
        fmt.Printf("err = %s", err)
    }

	wholeFunctions := []string {}

	ast.Inspect(node, func(n ast.Node) bool {
		res, ok := n.(*ast.CallExpr)
		if ok {
			fn := res.Fun
			if functionName, ok := fn.(*ast.Ident); ok{
				singleFunction := fmt.Sprintf("%s", functionName)
				wholeFunctions = append(wholeFunctions, singleFunction)
				fmt.Printf(" %s ", singleFunction)
				}
			if functionName,ok := fn.(*ast.SelectorExpr); ok{

				var wholeFunctionName string

				functionHead := functionName.Sel
				functionBody := functionName.X
				wholeFunctionName = fmt.Sprintf("%s", functionHead)
				
				// This code should be solved by loop, while I take the dark magic
				if subFunctionBody, okk := functionBody.(*ast.SelectorExpr); okk{
					wholeFunctionName = fmt.Sprintf("%s.%s", subFunctionBody.Sel, wholeFunctionName)
					subsubFunctionBody := subFunctionBody.X
					
					if aFunctionBody, okkk := subsubFunctionBody.(*ast.SelectorExpr); okkk{
						wholeFunctionName = fmt.Sprintf("%s.%s", aFunctionBody.Sel, wholeFunctionName)
						bFunctionBody := aFunctionBody.X
						
						// Add more due to the actual situation 
						if cFunctionBody, okkkk := bFunctionBody.(*ast.SelectorExpr); okkkk{
							wholeFunctionName = fmt.Sprintf("%s.%s", cFunctionBody.Sel, wholeFunctionName)
							dFunctionBody := cFunctionBody.X
							
							if finalFunctionBody, okkkkk := dFunctionBody.(*ast.SelectorExpr); okkkkk{
								wholeFunctionName = fmt.Sprintf("%s.%s", finalFunctionBody.Sel, wholeFunctionName)
								wholeFunctionName = fmt.Sprintf("%s.%s", finalFunctionBody.X, wholeFunctionName)
							} else {
								wholeFunctionName = fmt.Sprintf("%s.%s", dFunctionBody, wholeFunctionName)
							} 
						} else {
							wholeFunctionName = fmt.Sprintf("%s.%s", bFunctionBody, wholeFunctionName)
						}
					} else {
						wholeFunctionName = fmt.Sprintf("%s.%s", subsubFunctionBody, wholeFunctionName)
					}
				} else {
					wholeFunctionName = fmt.Sprintf("%s.%s", functionBody, wholeFunctionName)
				}
				if !strings.Contains(wholeFunctionName, "SelectorExpr") {
					wholeFunctions = append(wholeFunctions, wholeFunctionName)
					// This time I use stdout for logging
					fmt.Printf(" %s ", wholeFunctionName)
				}
			}
		}
		return true
	})
	return wholeFunctions
}

func removeRepSlice(slc []string) []string {
    result := []string{}         
    tempMap := map[string]byte{}
    for _, e := range slc {
        l := len(tempMap)
        tempMap[e] = 0 
        if len(tempMap) != l { 
            result = append(result, e)
        }
    }
    return result
}

func saveToJson(repoName string, data []string){
	tosaveData := []functionData{{repoName, data}}
    filePtr, err := os.Create("testFunctions.json")
    if err != nil {
        fmt.Println("Failed in creating json file", err.Error())
        return
    }
    defer filePtr.Close()

    encoder := json.NewEncoder(filePtr)
    err = encoder.Encode(tosaveData)
    if err != nil {
        fmt.Println("Error occur", err.Error())
    } else {
        fmt.Println("Save to json file success")
    }
}