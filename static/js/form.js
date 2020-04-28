  var mealsByCategory = {
    TC_1: ["TC_1_1", "TC_1_2", "TC_1_3"],
    TC_2: ["TC_2_1", "TC_2_2", "TC_2_3"],
    TC_3: ["TC_3_1", "TC_3_2", "TC_3_3"]
}

    function changecat(value) {
        if (value.length == 0) document.getElementById("testcase").innerHTML = "<option></option>";
        else {
            var catOptions = "";
            for (categoryId in mealsByCategory[value]) {
                catOptions += "<option>" + mealsByCategory[value][categoryId] + "</option>";
            }
            document.getElementById("testcase").innerHTML = catOptions;
        }
    }