import * as yup from 'yup';

import { t } from '../../i18n';

export const getUpdateAccountDetailsSchema = (nameMaxLength: number) => {
  return yup.object().shape({
    name: yup
      .string()
      .required(t('validation.required'))
      .max(nameMaxLength, t('validation.maxName', { max: nameMaxLength })),
  });
};

export const getChangePasswordSchema = (passwordMinLength: number, passwordMaxLength: number) => {
  return yup.object().shape({
    currentPassword: yup.string().required(t('validation.required')),
    newPassword: yup
      .string()
      .required(t('validation.required'))
      .min(passwordMinLength, t('validation.minPassword', { min: passwordMinLength }))
      .max(passwordMaxLength, t('validation.maxPassword', { max: passwordMaxLength })),
    repeatNewPassword: yup
      .string()
      .oneOf([yup.ref('newPassword'), null], t(`validation.passwordMatch`)),
  });
};
