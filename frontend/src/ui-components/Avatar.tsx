import Avatar, { AvatarProps } from '@mui/material/Avatar';

import { Account } from '../backendTypes';

interface AccountAvatarProps extends Omit<AvatarProps, 'alt' | 'src'> {
  account: Account | null;
}

export const AccountAvatar = ({ account, ...rest }: AccountAvatarProps) => (
  <Avatar alt="Account avatar" src={account?.avatar} {...rest}>
    {account?.name ? account?.name[0] : ''}
  </Avatar>
);
