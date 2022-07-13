import CloseIcon from '@mui/icons-material/Close';
import Box from '@mui/material/Box';
import Fade from '@mui/material/Fade';
import IconButton from '@mui/material/IconButton';
import BaseModal, { ModalProps as BaseModalProps } from '@mui/material/Modal';

type ModalProps = Omit<
  BaseModalProps,
  'closeAfterTransition' | 'keepMounted' | 'onClose' | 'sx'
> & {
  width: number | string;
  onClose: () => void;
};

export const Modal = ({
  'aria-labelledby': ariaLabelledBy,
  'aria-describedby': ariaDescribedBy,
  open,
  onClose,
  children,
  width,
  ...rest
}: ModalProps) => (
  <BaseModal
    aria-labelledby={ariaLabelledBy}
    aria-describedby={ariaDescribedBy}
    open={open}
    onClose={onClose}
    closeAfterTransition
    keepMounted
    sx={{ position: 'relative' }}
    {...rest}
  >
    <Fade in={open}>
      <Box
        sx={{
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: { width },
          bgcolor: 'background.paper',
          boxShadow: 24,
          p: 4,
        }}
        data-testid="modalContent"
      >
        <>
          <IconButton
            onClick={onClose}
            color="inherit"
            aria-label="close modal"
            sx={{ position: 'absolute', top: '5%', right: '5%' }}
          >
            <CloseIcon data-testid="closeIcon" />
          </IconButton>
        </>
        {children}
      </Box>
    </Fade>
  </BaseModal>
);
