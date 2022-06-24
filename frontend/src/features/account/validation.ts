import * as yup from 'yup';

import { t } from '../../i18n';

export const getUpdateAccountSchema = (nameMaxLength: number) => {
  return yup.object().shape({
    name: yup
      .string()
      .required(t('validation.required'))
      .max(nameMaxLength, t('validation.maxName', { max: nameMaxLength })),
  });
};
