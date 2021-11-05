import React, { useState } from 'react';
export interface ConsentFormProp {
  onEvent: any;
}

function ConsentForm({ onEvent }: ConsentFormProp) {
  const [checked11, setChecked11] = useState<boolean>(false);
  const [checked12, setChecked12] = useState<boolean>(false);
  const [checked21, setChecked21] = useState<boolean>(false);
  const [checked22, setChecked22] = useState<boolean>(false);
  const [checked31, setChecked31] = useState<boolean>(false);
  const [checked32, setChecked32] = useState<boolean>(false);
  const [error, setError] = useState<boolean>(false);

  function check11() {
    setChecked11(!checked11);
    setChecked12(false);
  }
  function check12() {
    setChecked12(!checked12);
    setChecked11(false);
  }
  function check21() {
    setChecked21(!checked21);
    setChecked22(false);
  }
  function check22() {
    setChecked22(!checked22);
    setChecked21(false);
  }
  function check31() {
    setChecked31(!checked31);
    setChecked32(false);
  }
  function check32() {
    setChecked32(!checked32);
    setChecked31(false);
  }

  function handleSubmit() {
    if (checked11 && checked21 && checked31) {
      onEvent();
    }
    else {
      setError(true);
    }
  }

  return (
    <div>
      <h2>Consent From</h2>
      <p>
        Note: This is a template for consent form. Add any additional information here.
      </p>

      <div>I am age 18 or older.
        <label style={{ marginLeft: "2rem" }}><input
          name="isGoing"
          type="checkbox"
          checked={checked11}
          onChange={check11} /> Yes</label>

        <label style={{ marginLeft: "1rem" }}><input
          name="isGoing"
          type="checkbox"
          checked={checked12}
          onChange={check12} /> No</label>
      </div><br />
      <div>I have read and understand the information above.
        <label style={{ marginLeft: "2rem" }}><input
          name="isGoing"
          type="checkbox"
          checked={checked21}
          onChange={check21} /> Yes</label>

        <label style={{ marginLeft: "1rem" }}><input
          name="isGoing"
          type="checkbox"
          checked={checked22}
          onChange={check22} /> No</label>
      </div><br />
      <div>I want to participate in this research and continue with the task.
        <label style={{ marginLeft: "2rem" }}><input
          name="isGoing"
          type="checkbox"
          checked={checked31}
          onChange={check31} /> Yes</label>

        <label style={{ marginLeft: "1rem" }}><input
          name="isGoing"
          type="checkbox"
          checked={checked32}
          onChange={check32} /> No</label>
      </div>
      <br />
      {error ?
        <p style={{ color: 'red' }}>You need to answer yes to all agreements to continue.
        </p>
        : null}
      <button style={{ marginBottom: "2rem" }} onClick={handleSubmit}> Submit </button>

    </div>

  );
}

export default ConsentForm;
