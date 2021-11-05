import React, {useState, } from 'react';
import ReactModal from 'react-modal';

import style from "./styles/TextViewer.module.css";
import TextAreaA from "./components/TextAreaA";
import TextAreaB from "./components/TextAreaB";

// @ts-ignore
import Progress from 'react-progressbar';
import {IAnnotation, ISinglePack,} from '../nlpviewer/lib/interfaces';
import {
  IMultiPack, IMultiPackQuestion,
} from "./components/lib/interfaces";
import {cross_doc_event_legend} from "./components/lib/definitions";
// @ts-ignore
import { useAlert } from 'react-alert'
import Select from 'react-select';
import {useHistory} from "react-router";

export type OnEventType = (event: any) => void;

export interface CrossDocProp {
  textPackA: ISinglePack;
  textPackB: ISinglePack;
  multiPack: IMultiPack;
  multiPackQuestion:  IMultiPackQuestion;
  onEvent: OnEventType;
  nextID: string;
  secretCode: string;
}
export default function IndexAnnotationViewer(props: CrossDocProp) {

  const history = useHistory();

  const {textPackA, textPackB, multiPack, multiPackQuestion, onEvent, nextID, secretCode} = props;


  // @ts-ignore
  let options = multiPack.creation_records.map((record) => ({
    value: record.forteID,
    label: record.forteID,
  }));
  if (options.length == 0) {
    options = [{
      value: "No Annotator",
      label: "No Annotator",
    }]
  }

  const [selectedForteID, setSelectedForteID] =  useState(options[0]);

  // @ts-ignore
  const my_annotation = options[0].value !== "No Annotator"? multiPack.creation_records.find(ele => ele.forteID===selectedForteID.value).records
  : [];
  let annotationsA = textPackA.annotations;
  let annotationsB = textPackB.annotations;
  annotationsA.sort(function(a, b){return a.span.begin - b.span.begin});
  annotationsB.sort(function(a, b){return a.span.begin - b.span.begin});

  const all_events_A : IAnnotation[] = annotationsA.filter((entry:IAnnotation)=>entry.legendId === cross_doc_event_legend);
  const all_events_B : IAnnotation[] = annotationsB.filter((entry:IAnnotation)=> entry.legendId === cross_doc_event_legend);
  // textPackA.annotations = all_events_A;
  // textPackB.annotations = all_events_B;


  const [AnowOnEventIndex, setANowOnEventIndex] =  useState<number>(0);
  const [BnowOnEventIndex, setBNowOnEventIndex] =  useState<number>(-1);

  const nowAOnEvent = all_events_A[AnowOnEventIndex];
  const nowBOnEvent = all_events_B[BnowOnEventIndex];

  // @ts-ignore
  const BSelectedIndex = multiPack.crossDocLink.filter(item => item._parent_token === +nowAOnEvent.id && item.coref==="coref" && my_annotation.includes(item.id))
            .map(item => item._child_token)
            .map(event_id => all_events_B.findIndex(event => +event.id===event_id));

  const [nowQuestionIndex, setNowQuestionIndex] =  useState<number>(-1);
  const now_question = nowQuestionIndex >=0 ? multiPackQuestion.coref_questions[nowQuestionIndex] : undefined;

  // @ts-ignore
  let now_question_anno = null;

  if (now_question){
    // all question answers for current event pair for current annotator
    // @ts-ignore
    const temp_anno = multiPack.crossDocLink.find(item => item._parent_token === +nowAOnEvent.id && item._child_token === +nowBOnEvent.id && item.coref==="coref" && my_annotation.includes(item.id))
                .coref_answers;
    // @ts-ignore
    now_question_anno = temp_anno.find(item => item.question_id === now_question.question_id)
  }
  console.log(now_question_anno);


  const BackEnable: boolean =  AnowOnEventIndex > 0;
  const nextEventEnable:boolean = AnowOnEventIndex < all_events_A.length;
  const progress_percent = Math.floor(AnowOnEventIndex / all_events_A.length * 100);

  const [finished, setFinished] = useState<boolean>(false);


  const alert = useAlert();

  const customStyles = {
    // @ts-ignore
    option: (provided, state) => ({
      ...provided,
      borderBottom: '2px dotted green',
      color: state.isSelected ? 'yellow' : 'black',
      backgroundColor: state.isSelected ? 'green' : 'white',
    }),
    // @ts-ignore
    control: (provided) => ({
      ...provided,
      marginTop: "5%",
    })
  };



  function clickNextEvent() {

    if (AnowOnEventIndex === all_events_A.length-1) {
      if (nextID !== "None"){
        history.push('/crossdocs/'+nextID);
      }
      else {
        setFinished(true);
      }
    } else {
      setANowOnEventIndex(AnowOnEventIndex + 1);
      setBNowOnEventIndex(-1);
      setNowQuestionIndex(-1);
    }

  }

  function clickBack() {
    setANowOnEventIndex(AnowOnEventIndex-1);
    setBNowOnEventIndex(-1);
    setNowQuestionIndex(-1);

  }


  // this function is triggered when any event is clicked
  function eventClickCallBack(eventIndex:number, selected:boolean){
    if (multiPackQuestion.coref_questions.length === 0) {
      return
    }

    // only show questions for annotated event
    if (BSelectedIndex.includes(eventIndex)) {
        setBNowOnEventIndex(eventIndex);
        setNowQuestionIndex(0);
        return
    }
  }
  function handleForteIDChange(newForteID : any) {
    setSelectedForteID(newForteID);
    setBNowOnEventIndex(-1);
    setNowQuestionIndex(-1);
  }

  function clickPrevQ() {
     if (nowQuestionIndex > 0) setNowQuestionIndex(nowQuestionIndex-1);
  }
  function clickNextQ() {
     if (nowQuestionIndex < multiPackQuestion.coref_questions.length-1) setNowQuestionIndex(nowQuestionIndex + 1);
  }



  return (
      <div>
        <ReactModal isOpen={finished} className={style.modal} overlayClassName={style.modal_overlay}>You have finished. Secret code is {secretCode}</ReactModal>
      <div className={style.text_viewer}>
        {/*discription here*/}
        <div className={style.tool_bar_container}>
          <div className={style.spread_flex_container}>
            <div>You are in a view-only mode</div>
          </div>
        </div>


        {/*next event and document*/}
        <div className={style.second_tool_bar_container}>
          <div>
            <button disabled={!BackEnable} onClick={clickBack}
                    className={style.button_next_event}>
              Back
            </button>
            <button disabled={!nextEventEnable} onClick={clickNextEvent}
                    className={style.button_next_event}
            > Next event
            </button>
            <label><Progress completed={progress_percent} />Progress: {progress_percent}%</label>
            {/*<div className={style.button_action_description}>*/}
            {/*  Click next event only if you have finished this event*/}
            {/*</div>*/}

          </div>
          <div className={style.answer_box}>
              {now_question ?
                <div>
                  <div>
                    <button onClick={clickPrevQ}>
                      Prev Q
                    </button>
                    <button onClick={clickNextQ}>
                      Next Q
                    </button>
                  </div>
                  <div className={style.question_container}>
                    {now_question.question_text}
                  </div>
                  <div className={style.option_container}>
                    {now_question.options.map(option => {
                      return (
                         // @ts-ignore
                        <button className={option.option_id === now_question_anno.option_id ? style.button_option_alert : style.button_option} key={option.option_id}>
                          {option.option_text}
                        </button>
                      )
                    })}
                  </div>
                </div>
                : null}
          </div>
          <div style={{width:"500px", marginTop:"-5em"}}>
          <Select styles={customStyles} options={options} onChange={handleForteIDChange}  value={selectedForteID}/>
          </div>

        </div>


        <main className={style.layout_container}>

          <div
              className={`${style.center_area_container}`}
          >

            <div className={`${style.text_area_container}`}>
              <TextAreaA
                  text = {textPackA.text}
                  annotations={all_events_A}
                  NER={[]}
                  AnowOnEventIndex={AnowOnEventIndex}
              />
            </div>
          </div>

          <div
              className={`${style.center_area_container}`}
          >
            <div className={`${style.text_area_container}`}>
              <TextAreaB
                  text = {textPackB.text}
                  annotations={all_events_B}
                  NER = {[]}
                  AnowOnEventIndex={AnowOnEventIndex}
                  BnowOnEventIndex={BnowOnEventIndex}
                  BSelectedIndex={BSelectedIndex}
                  eventClickCallBack={eventClickCallBack}
              />
            </div>
          </div>


        </main>
      </div>
      </div>
  );
}

