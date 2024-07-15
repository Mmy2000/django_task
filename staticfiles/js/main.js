const modalBtn = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('startBtn')
const url = window.location.href
const submitBtn = document.getElementById('submitBtn')
modalBtn.forEach(modalBtn => modalBtn.addEventListener("click" , ()=>{

    const pk = modalBtn.getAttribute('data-pk')
    const name = modalBtn.getAttribute('data-quiz')
    const question = modalBtn.getAttribute('data-questions')
    const difficulty = modalBtn.getAttribute('data-difficulty')
    const time = modalBtn.getAttribute('data-time')
    const score = modalBtn.getAttribute('data-pass')
    
    modalBody.innerHTML = `<div class="mb-3">Are you sure you want to begin "<b>${name}</b>"?</div>
    <div class="text-muted">
    <ul>
    <li>Difficulty: <b>${difficulty}</b></li>
    <li>number of question: <b>${question}</b></li>
    <li>score to pass: <b>${score}%</b></li>
    <li>Time: <b>${time} min</b></li>
    </ul>
    </div>`
    startBtn.addEventListener('click' , ()=>{
        window.location.href = url + pk    })
}) 
    
);

// data auiz view
const quizBox = document.getElementById('quizBox')
const quizForm = document.getElementById('quiz-form')
const scoreBox = document.getElementById('scoreBox')
const resultBox = document.getElementById('resultBox')
const timerBox = document.getElementById('timerBox')
const csrf = document.querySelector('[name=csrfmiddlewaretoken]')
let timer = 0;
const activateTimer = (time)=>{
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    }else{
        timerBox.innerHTML = `<b>${time}:00</b>`
    }
    let minutes = time - 1
    let seconds = 60
    let displayMinutes
    let displaySecond

     timer = setInterval( ()=>{
        seconds --
        if (seconds < 0 ) {
            seconds = 59,
            minutes --
        }
        if (minutes.toString().length < 2) {
            displayMinutes = "0"+minutes
        }else{
            displayMinutes = minutes
        }
        if (seconds.toString().length < 2) {
            displaySecond = '0'+seconds
        }else{
            displaySecond = seconds
        }
        if (minutes === 0 && seconds ===0) {
            timerBox.innerHTML = '<b>00:00</b>'
            setTimeout(()=>{
                clearInterval(timer)
            alert("Time Over")
            sendData()          
            })
        // if (sendData() == true) {
        //     clearInterval(timer)
        //     console.log("hello");
        // }
            
        }
        timerBox.innerHTML = `<b>${displayMinutes}:${displaySecond}</b>`
    },1000)
    

}

$.ajax({
    type: "GET",
    url: `${url}data`,
    success: function (response) {
        const data = response.data
        if (response.existing === false) {
            data.forEach(el =>{
            for (const [question , answers] of Object.entries(el)) {
                quizBox.innerHTML += `
                    <hr>
                    <div class="mb-3">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer => {
                    quizBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>
                    `
                });
            }
        })
        activateTimer(response.time)
        }else{
                resultBox.innerHTML = `
                <div id="message" class="container">
                <div class="alert alert-danger" role="alert">
                    you already Taked this Quiz.
                </div>
                </div>
            `            
            quizForm.classList.add('d-none')
        }
        
    },
    error:function(error){
        console.log(error);
    }
});

const sendData = () =>{
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf.value
    elements.forEach(el=>{
        if (el.checked) {
            data[el.name] = el.value
        } else{
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })
    $.ajax({
        type:"POST",
        url:`${url}save/`,
        data:data,
        success:function(response){
            
            const results = response.results
            quizForm.classList.add("d-none")

            scoreBox.innerHTML = `${response.passed ? 'Congratulations ' : 'Ops..:( '}Your result is ${response.score.toFixed(2)}%`
///



            results.forEach(res=>{
                const resDev = document.createElement('dev');

                for (const [question , resp] of Object.entries(res)){
        
                    resDev.innerHTML += question
                    const cls = ['container' ,'d-flex' , 'p-3' , 'text-light' , 'h5']
                    resDev.classList.add(...cls)

                    if (resp == "not answered"){
                        resDev.innerHTML += '- not answered'
                        resDev.classList.add('bg-danger')
                    }else{
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                        if (answer == correct) {
                            resDev.classList.add('bg-success')
                            resDev.innerHTML += ` answered : ${answer}`
                        }else{
                            resDev.classList.add('bg-danger')
                            resDev.innerHTML += ` | correct : ${correct}`
                            resDev.innerHTML += ` | answered : ${answer}`
                        }
                    }
                }
                // const body = document.getElementsByTagName('BODY')[0]
                resultBox.append(resDev)
                clearInterval(timer)
                
            })
        },
        error:function(error){
            console.log(error);
        }
    })
}

quizForm.addEventListener('submit' , e=>{
    e.preventDefault()
    sendData()
})

setTimeout(function(){
    $('#message').fadeOut('slow')
},4000)