import React, { useRef, useEffect, useState } from 'react';
import style from '../styles/CrossDocStyle.module.css';
import openInstructionGif from '../images/instructions_examples.gif';
import PairGif from '../images/pair_annotation.gif';
import DeleteAnno from '../images/remove_annotation.gif';
import NextEventGif from '../images/next_event.gif';

function Instruction() {
  return (
    <div>
      <h1>Instructions for using the tool</h1>
      <p>This tool can be used to select events that are the same across the two given documents.</p>

      <p>At any point during the task, you can click on the “View Instructions” button to read these instructions.</p>

      <h3>What is this task about?</h3>
      <ul>
        <li style={{ marginBottom: "5px" }}>Two related documents are presented side-by-side on the tool.</li>
        <li style={{ marginBottom: "5px" }}>A few words in both the documents are underlined and these are referred to as events.</li>
        <li style={{ marginBottom: "5px" }}>The task is to select events from the right document that are the same as the currently highlighted event in the left document.</li>
      </ul>

      <h3>How should I solve this task?</h3>
      <ul>
        <li style={{ marginBottom: "5px" }}>When you first start the task, make sure you read through both the left and right documents to get an overall understanding of the two documents.</li>
        <li style={{ marginBottom: "5px" }}>At each step, an event is highlighted in a blue box on the left document (aka. <i>target event</i>). Now, your goal is to identify underlined events from the right document that are the same as the target event from the left document.</li>
        <li style={{ marginBottom: "5px" }}>Once you select an event from the right document (an annotation), you are presented a few follow-up questions. Make sure you answer these questions to the best of your knowledge.</li>
        <li style={{ marginBottom: "5px" }}>If you change your mind while answering the questions, you can click the “Cancel” button to remove your annotation.</li>
        <li style={{ marginBottom: "5px" }}>After you have identified all possible same events from the right document (if any), please use the “Next event” button to move to the next target event on the left document.</li>
      </ul>

      <h3>FAQs</h3>
      <p><b>Q:</b> I made a mistake and incorrectly marked two events as the same. How do I correct this?</p>
      <p style={{ marginLeft: "2em" }}>If you are still answering the follow-up questions, you can just click on the “Cancel” button.
        <br />
        If you have already moved to the next target event, you can use the “Back” button to move back the previously finished target events.
      </p>

      <p><b>Q:</b> I am not sure how to respond to the follow-up questions. How should I proceed?</p>
      <p style={{ marginLeft: "2em" }}>The follow-up questions help us understand more about your decision that two events are the same. It is <b>important</b> to note that the response to these questions need not always be “Yes”. In fact, in many cases, you may not have enough information to respond with a definite “Yes” or “No”, then please feel free to select “Not enough information”.</p>


      <p><b>Q:</b> How do I decide if two events are the same or different?</p>
      <p style={{ marginLeft: "2em" }}>We understand that this decision is not always easy. To help you with this, we compiled a bunch of examples. You can quickly glance through them using the “View Examples” button on the tool.</p>

      <p> For any comments, feedback and/or suggestions, contact the authors. </p>

    </div>
  );
}



export default Instruction;
