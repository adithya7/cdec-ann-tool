import React, {useRef, useEffect, useState} from 'react';
import style from '../styles/CrossDocStyle.module.css';

function Example() {
  return (
    <div>
      <h1>Examples</h1>
      <h3>Goal of the Task</h3>
      <p>You will help us identify the same events from different documents.</p>

      <h3>What is an event?</h3>
      <p>People use text to describe what happen(ed) in the world. These are called events in text. We often use verbs, sometimes even (pro)nouns, and adjectives as <u><b>events</b></u>. For example:</p>
      <p className={style.paragraph_indent}>	It <u><b>rained</b></u> a lot yesterday.</p>
      <p className={style.paragraph_indent}>There was a <u><b>fire</b></u> last night.</p>
      <p className={style.paragraph_indent}>He <u><b>got sick</b></u>. </p>

      <h3>How do we know that the two events are the same?</h3>
      <p>In the following examples (1 to 5), two events are the same.</p>
      <ol>
        <li>
          When two events refer to the same thing, they should be the same in terms of meaning, or semantically identical. <br/>
          <ol type="a">
            <li>Taken as a whole, the evidence suggests that the plan to <u><b>bomb</b></u> the Boston Marathon took shape over three months.</li>
            <li>Dzhokhar Tsarnaev apologized for suffering caused by the Boston Marathon <u><b>bombing</b></u>.</li>
          </ol>
        </li>
        <br/>
        <li>When two events are the same, one event may be the synonym for the other.<br/>
          <ol type="a">
            <li>A 16- year-old southern Utah boy was <u><b>accused</b></u> of bringing a homemade bomb to his high school. </li>
            <li>The teen was <u><b>charged</b></u> Monday with attempted murder and use of a weapon of mass desctuction, both first-degreen felonies.</li>
          </ol>
        </li>
        <br/>
        <li>Sometimes one event may be the pronoun (e.g.,it) or the anaphora (e.g., this, that) of the other, when they are the same.<br/>
          <ol type="a">
            <li>Both drones carried explosives, and no YPF (“People’s Defence Units”)  fighters were injured in the <u><b>incident</b></u>.</li>
            <li><u><b>This</b></u> would not be the first terrorist drone strike.</li>
          </ol>
        </li>
        <br/>
        <li>The same events do not have to take place at the same time. In the following example, one event (‘go”) would happen in the future, while the other (“went”) did occur.<br/>
          <ol type="a">
            <li>The couple had been planning to <u><b>go</b></u> to Paris for a long time.</li>
            <li>They finally <u><b>went</b></u> there last month.</li>
          </ol>
        </li>
        <br/>
        <li>Sometimes the same events are described from different perspectives. The following example refers to the exchange of the gift from two perspectives.<br/>
          <ol type="a">
            <li>John <u><b>gave</b></u> a gift to Mary.</li>
            <li>Mary <u><b>received</b></u> a gift from John.</li>
          </ol>
        </li>
      </ol>

      <p>In the following examples (6 to 8), two events are not the same.</p>
      {/*
      // @ts-ignore*/}
      <ol start="6">
        <li>
            When one event is a part of the other larger event, they are not the same. <br/>
            <ol type="a">
              <li>Following  the trial of Mahammed Alameh, the first suspect in the <u><b>bombing</b></u>, investigators discovered a jumble of chemicals, chemistry implements and detonating materials.</li>
              <li>The <u><b>explosion</b></u> killed at least five people. (“bombing” refers to the entire process which starts with making a bomb and ends with destructions, damages and injuries, while “explosion” is a smaller event that occurs in that processes)</li>
            </ol>
        </li>
        <br/>
        <li>Two events are not the same even if they are the same semantically. The first example refers to the general bomb-making process, while the second one indicates a particular bomb-making event that took place in the garage.<br/>
            <ol type="a">
              <li>They obtained the online manual of bomb-<u><b>making</b></u>. (general bomb-making process)</li>
              <li>They <u><b>made</b></u> a bomb in the garage. (specific bomb-making event that happened in the specific place)</li>
            </ol>
        </li>
        <br/>
        <li>When one event consists of, or is a member of the other event, they are not the same. The first example refers to the specific death of a 44-year-old man, while the second one refers to the deaths of 305 people.<br/>
            <ol type="a">
              <li>The government announced that a 44-year-old man <u><b>died</b></u> from the COVID. (death of a 44-year-old man)</li>
              <li>There are more than 14,300 confirmed COVID cases, and 305 people have <u><b>died</b></u>. (deaths of 305 people)</li>
            </ol>
        </li>
    </ol>




    </div>
  );
}



export default Example;
