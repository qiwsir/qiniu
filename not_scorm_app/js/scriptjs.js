answers = {};
questions = 0; 	//题目数量
//answers = {
//	"1": {
//		"answer": [A,],
//		"do_answer": [B,],
//		"style": "single_option",
//		"result": false,
//	}
//}

//点击提交按钮
$(function(){
	$("#question_btn").click(function(){
		//right_answer(); 		//从网页的设置中得到所有题目的正确答案
		var check_result = check_user_answers();
		if (check_result>0){ 	//题目都已经回答
			var right_user_answers = check_result - 1;
			//根据规则显示用户是否通过考试
			var test_result = pass_test(questions, right_user_answers);
			if (test_result){		//通过考试
				$("#video").css("display", "none");
				$("#notpass").css("display", "none");
				$("#error").css("display", "none");
				$("#testnote").css("display", "none");
				$("#passinfo").css("display", "block");
				$("#passinfo").html("<div class='maincontent'><p class='pinfo'>你已经完成本次课程学习，并通过了测试。</p><p class='pinfo'>下面是你的测试结果</p></div>");
				$(".rightanswer").css("display", "block");
				$("#question_btn").css("display", 'none');
				scoFinished();
			}else{		//未通过考试
				$("#notpass").css("display", "block");
				$("#error").css("display", "none");
			}
		}else{ 		//尚有题目未回答
			$("#error").css("display", "block");
			$("#notpass").css("display", "none");
		}
	});
});

function loadPage(){
	right_answer();
}
//获得所有题目的标准答案
function right_answer(){
	var problems = $(".question");
	questions = problems.length
	for (var i=0; i<problems.length; i++){
		var this_answer = {};
		var problem_style = problems[i].children[0]["className"]; 		//题目类型
		var problem_number = problems[i].children[0].children[0].children[0].children[0].innerHTML; 		//题号
		var problem_answer = problems[i].children[0].children[1].children[0].innerHTML; 		//标准答案
		var problem_answer_lst = problem_answer.split(",");
		this_answer["style"] = problem_style;
		this_answer["answer"] =problem_answer_lst;
		this_answer['do_answer'] = ' ';
		answers[problem_number] = this_answer;
	}
}

//用户的选择题结果
$(function(){
	$("input").click(function(){
		var pNode = $(this).parents("div.question");
		var qNum = $(pNode).find("span.number").html();
		//alert(qNum);
		var result = [];
		pNode.find("input").each(function(){
			if($(this).attr("checked")){
				//alert($(this).val());
				result .push($(this).val() );
			}
		answers[qNum]["do_answer"] = result;
		});
	});
});
//匹配题结果
$(function(){
	$("select").change(function(){
		var pNode = $(this).parents("div.question");
		var qNum = $(pNode).find("span.number").html();
		//alert(qNum)
		var result = [];
		pNode.find("option").each(function(){
			if($(this).attr("selected")){
				result.push($(this).val());
			}
		answers[qNum]["do_answer"] = result;
		})
	})
})

//判断用户回答的结果是否正确，并保存判断结果
function check_user_answers(){
	var i = 1;
	for (var problem_number in answers){
		if (answers[problem_number]['do_answer']==" "){ 	//如果没有回答完毕，返回false
			return false;
		}else{
			//判断是否正确并将结果记录
			right_answer = answers[problem_number]['answer'].join();
			user_answer = answers[problem_number]['do_answer'].join();
			if (right_answer == user_answer){
				answers[problem_number]['result'] = true;
				i += 1;
			}else{
				answers[problem_number]['result'] = false;
			}
		}
	}
	return i;
}

//判断是否通过考试的标准（如果大于等于10个题目，正确率为80%为通过，如果小于10个题目，必须全部答对才能通过）
function pass_test(questions_number, right_answers_number){
	if (questions_number < 10){
		if (questions_number == right_answers_number){
			return true;
			}else{
				return false;
			}
	}else{
		rate = (questions_number*0.8).toFixed(1);
		if (right_answers_number >= rate){
			return true;
		}else{
			return false;
		}
	}
}


//非scorm标准的函数
function scoFinished(){
    //alert("您已完成本sco学习！")
	App.call("doMobileSetValue", "cmi.core.lesson_status", "completed",function(e){
		alert(e);
	})
	App.call("doMobileCommit")
}
