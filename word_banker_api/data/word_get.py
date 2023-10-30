def word_options(text, to_lang):    from googletrans import Translator    translator = Translator()    translated_text = translator.translate(text, dest=to_lang)    word_info = {}    word_info['text'] = text    word_info['mainly-translate'] = translated_text.text    all_translates = translated_text.extra_data['all-translations']    word_info['translates'] = []    if all_translates is not None:        i = 0        for trs in all_translates:            word_info['translates'].append({'type': trs[0], 'words': trs[1]})            i += 1    try:        set_let = []        word_info['definitions'] = []        if to_lang == 'uz':            for definitions in translated_text.extra_data['definitions']:                word_types = definitions[0]                means = definitions[1]                means_list = []                for word_mean in means:                    word_mean_use = word_mean[0]                    word_mean_use_uz = (translator.translate(word_mean_use, 'uz')).text                    if len(word_mean) == 2:                        example = None                        example_uz = None                    else:                        example = word_mean[2]                        example_uz = (translator.translate(example, 'uz')).text                    means_list.append({'word-mean': word_mean_use,                                       'example': example,                                       'word-mean-uz': word_mean_use_uz,                                       'example-uz': example_uz                                       })                set_let.append(                    {                        'word-types': word_types,                        'word-means': means_list                    }                )            word_info['definitions'] = set_let        else:            for definitions in translated_text.extra_data['definitions']:                word_types = definitions[0]                means = definitions[1]                means_list = []                for word_mean in means:                    word_mean_use = word_mean[0]                    if len(word_mean) == 2:                        example = None                    else:                        example = word_mean[2]                    means_list.append({'word-mean': word_mean_use,                                       'example': example                                       })                set_let.append(                    {                        'word-types': word_types,                        'word-means': means_list                    }                )            word_info['definitions'] = set_let    except:        pass    try:        word_info['synonyms'] = []        all_synonyms = []        for synonym in translated_text.extra_data['synonyms']:            synonym_type = synonym[0]            synonym_words = synonym[1]            synonym_words_all = []            for synonym_word in synonym_words:                for synonym_group in synonym_word[0]:                    synonym_words_all.append(synonym_group)            all_synonyms.append(                {                    'synonym-type': synonym_type,                    'synonyms': synonym_words_all                }            )        word_info['synonyms'] = all_synonyms    except:        pass    try:        word_info['examples'] = []        for example in translated_text.extra_data['examples'][0]:            word_info['examples'].append(example[0])    except:        pass    return word_info