
var dataVideos = []
var settingsTypes = []
var users = []
var statistics = {}
const TOP_VID = 5


function createReport1(){
    var str = ""
    for (const key in statistics) {
        if (Object.hasOwnProperty.call(statistics, key)) {
            str+=`<h5> ${key} : ${statistics[key]} </h5>`;
            
        }
    }
    return `<h3>Users priority</h3>
            ${str}`
}

function createReport2(){
    var sumObj ={}
    for (let i = 0; i < settingsTypes.length; i++) {
        sumObj[settingsTypes[i]] = 0;   
    }

    for (let j = 0; j < dataVideos.length; j++) {
        if (Object.hasOwnProperty.call(sumObj, dataVideos[j].type)) {
            sumObj[dataVideos[j].type]++; 
            
        }       
    }   
    var str = ""
    for (const key in sumObj) {
        if (Object.hasOwnProperty.call(sumObj, key)) {
            str+=`<h5> ${key} : ${sumObj[key]} </h5>`;
            
        }
    }
    return `<h3>count of all videos by types</h3>
           ${str}`
}

function createReport3(top){
    
    
    dataVideos.sort((a,b) => b.avgRating - a.avgRating )
    
    var str ="" 

    for (let i = 0; i < top; i++) {
        str+=`<h5> ${i+1}) Rating: ${dataVideos[i].avgRating}    title: ${dataVideos[i].title}</h5>`
        
    }

    


    return `<h3>Top ${top} Rated videos</h3>
    ${str}`
}

async function isUserHasComments(strcol){
    var comments = []
    await db.collection(strcol).get().then((querySnapshot) => {
        querySnapshot.forEach((doc) => {
          
           comments.push(doc.id)
        });
         
    });

    return (comments.length > 0)
}

async function createReport4(){
   
    var active = 0 ;

    for (let index = 0; index < users.length; index++) {
        
        await isUserHasComments(`users/${users[index].docId}/ratedVideos`).then(res => {
            console.log(res)
            if(res){
                active++;
            }
        }).catch(err=>console.log(err))
            
        
        
    }

    return `<h3>Users report</h3>
            <h5>number of users : ${users.length}</h5>
            <h5>number of users that commented on videos : ${active}</h5>`
}

function showOnMonitor(){
   
    const r1 = document.getElementById("report1")
    const r2 = document.getElementById("report2")
    const r3 = document.getElementById("report3")
    const r4 = document.getElementById("report4")
    r1.innerHTML = createReport1()
    r2.innerHTML = createReport2()
    r3.innerHTML = createReport3(TOP_VID)
    createReport4().then(res => {
        r4.innerHTML = res
    }).catch(err => {r4.innerHTML = err} )
    
}

async function getAllInfo(){

   await db.collection("videos").get().then((querySnapshot) => {
        querySnapshot.forEach((doc) => {
           // console.log(`${doc.id} => ${doc.data()}`);
           dataVideos.push(doc.data())
        });

       
    });


    await db.collection("settings").get().then((querySnapshot) => {
        querySnapshot.forEach((doc) => {
           // console.log(`${doc.id} => ${doc.data()}`);
           settingsTypes.push(doc.id)
        });
         
    });

    await db.collection("users").get().then((querySnapshot) => {
        querySnapshot.forEach((doc) => {
           //console.log(`${doc.id} => ${doc.data()}`);
           users.push({docId : doc.id })
        });
         
    });

    await db.collection("statistics").get().then((querySnapshot) => {
        querySnapshot.forEach((doc) => {
          // console.log(`${doc.id} => ${doc.data()}`);
          statistics = {...doc.data()}
        });

        
         
    });


    showOnMonitor();

}

getAllInfo()





