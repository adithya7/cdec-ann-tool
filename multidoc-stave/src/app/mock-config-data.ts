import { IOntology } from '../nlpviewer';

export const ontology: IOntology = {
  ontologyName: 'forte.data.ontology.ontonotes_ontology',
  imports: ['forte.data.ontology.top'],
  entryDefinitions: [
    {
      entryName: 'forte.data.ontology.base_ontology.Token',
      parentEntryName: 'forte.data.ontology.top.Annotation',
      attributes: [
        {
          name: 'pos_tag',
          type: 'str',
        },
      ],
    },
    {
      entryName: 'forte.data.ontology.base_ontology.Sentence',
      parentEntryName: 'forte.data.ontology.top.Annotation',
    },
    {
      entryName: 'forte.data.ontology.base_ontology.Document',
      parentEntryName: 'forte.data.ontology.top.Annotation',
    },
    // {
    //   entryName: 'forte.data.ontology.ontonotes_ontology.PredicateMention',
    //   parentEntryName: 'forte.data.ontology.top.Annotation',
    // },
    {
      entryName: 'forte.data.ontology.base_ontology.PredicateArgument',
      parentEntryName: 'forte.data.ontology.top.Annotation',
    },
    {
      entryName: 'forte.data.ontology.base_ontology.PredicateLink',
      parentEntryName: 'forte.data.ontology.top.Link',
      parentType: 'forte.data.ontology.ontonotes_ontology.PredicateMention',
      childType: 'forte.data.ontology.base_ontology.PredicateArgument',
      attributes: [
        {
          name: 'arg_type',
          type: 'str',
        },
      ],
    },
    {
      entryName: 'forte.data.ontology.base_ontology.CoreferenceMention',
      parentEntryName: 'forte.data.ontology.top.Annotation',
    },
    {
      entryName: 'forte.data.ontology.base_ontology.CoreferenceGroup',
      parentEntryName: 'forte.data.ontology.top.Group',
      memberType: 'forte.data.ontology.base_ontology.CoreferenceMention',
    },
    {
      entryName: 'forte.data.ontology.base_ontology.CoreferenceGroup2',
      parentEntryName: 'forte.data.ontology.top.Group',
      memberType: 'forte.data.ontology.base_ontology.CoreferenceMention',
    },
    {
      entryName: 'forte.data.ontology.base_ontology.EntityMention',
      parentEntryName: 'forte.data.ontology.top.Annotation',
      attributes: [
        {
          name: 'ner_type',
          type: 'str',
        },
      ],
    },
    {
      entryName: 'forte.data.ontology.ontonotes_ontology.Token',
      parentEntryName: 'forte.data.ontology.base_ontology.Token',
      attributes: [
        {
          name: 'sense',
          type: 'str',
        },
      ],
    },
    {
      entryName: 'forte.data.ontology.ontonotes_ontology.Sentence',
      parentEntryName: 'forte.data.ontology.base_ontology.Sentence',
      attributes: [
        {
          name: 'speaker',
          type: 'str',
        },
        {
          name: 'part_id',
          type: 'str',
        },
      ],
    },
    {
      entryName: 'forte.data.ontology.ontonotes_ontology.PredicateMention',
      parentEntryName: 'forte.data.ontology.top.Annotation',
      attributes: [
        {
          name: 'pred_type',
          type: 'str',
        },
        {
          name: 'pred_lemma',
          type: 'str',
        },
        {
          name: 'framenet_id',
          type: 'str',
        },
      ],
    },
  ],
  constraints: {
    /**
     *
     * Token's attribute 'pos_tag', only contains 'pt1', 'pt2', 'pt3', 'pt4'
     *
     */
    'forte.data.ontology.base_ontology.Token': [
      {
        attributes: {
          pos_tag: ['pt1', 'pt2', 'pt3', 'pt4'],
        },
      },
    ],

    /**
     *
     * PredicateMention's attribute 'pred_type', only contains 'pt1', 'pt2', 'pt3', 'pt4'
     *
     */

    'forte.data.ontology.ontonotes_ontology.PredicateMention': [
      {
        attributes: {
          pred_type: ['pt1', 'pt2', 'pt3', 'pt4'],
        },
      },
    ],

    /**
     *
     * PredicateLink's parentType must be entry that
     *  - has legendId 'forte.data.ontology.ontonotes_ontology.PredicateMention'
     *  - attributes pred_type to be 'pt1' or 'pt2'
     * also childType must be entry that
     *  - has legendId 'forte.data.ontology.base_ontology.PredicateArgument
     *
     * PredicateLink can also be that, parentType must be entry that
     *  - has legendId 'forte.data.ontology.ontonotes_ontology.PredicateMention'
     *  - attributes pred_type to be 'pt3' or 'pt4'
     * also childType must be entry that
     *  - has legendId 'forte.data.ontology.base_ontology.Token
     *
     */

    'forte.data.ontology.base_ontology.PredicateLink': [
      {
        parentType: {
          legendId: ['forte.data.ontology.ontonotes_ontology.PredicateMention'],
          attributes: {
            pred_type: ['pt1', 'pt2'],
          },
        },
        childType: {
          legendId: ['forte.data.ontology.base_ontology.PredicateArgument'],
        },
      },
      {
        parentType: {
          legendId: ['forte.data.ontology.ontonotes_ontology.PredicateMention'],
          attributes: {
            pred_type: ['pt3', 'pt4'],
          },
        },
        childType: {
          legendId: ['forte.data.ontology.base_ontology.Token'],
        },
      },
    ],
  },
};
