export interface ICrossDocLink {
    // link id is always a number
    // update: changed to string since uuid is too long for javascript
    id: string|undefined;
    _parent_token: number;
    _child_token: number;
    coref: string;
    coref_answers: ICrossDocLinkAnswer[];
    suggested_answers: ICrossDocLinkAnswer[];
}
export interface ICrossDocLinkAnswer {
    question_id: string;
    option_id: number;
}

export interface ICreationRecordPerson {
    forteID: string;
    records: number[];
}

export interface IMultiPack {
    _parent_doc: number;
    _child_doc: number;
    crossDocLink : ICrossDocLink[];
    suggestedLink: ICrossDocLink[];
    creation_records: ICreationRecordPerson[];
}


export interface IMultiPackQuestion {
    coref_questions: IQuestion[];
    suggest_questions: IQuestion[];
}

export interface IQuestion {
    question_id: string;
    question_text:string;
    options: IOption[];
}
export interface IOption{
    option_id: number;
    option_text: string;
}
export interface IRange {
    start: number;
    end: number;
    color?: string;
}
