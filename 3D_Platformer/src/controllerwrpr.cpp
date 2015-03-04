#include "stdafx.h"
#include "controllerwrpr.h"


namespace ssuge {

	ControllerWrpr::ControllerWrpr() {}


	void ControllerWrpr::OnAxisMotion(SDL_Event evt) {
		//TODO: Implement dead zones
		switch(evt.caxis.axis) {
		case SDL_CONTROLLER_AXIS_LEFTX:
			std::cout << "Left Stick X: "<< evt.caxis.value << std::endl;
			break;
		case SDL_CONTROLLER_AXIS_LEFTY:
			std::cout << "Left Stick Y: " << evt.caxis.value << std::endl;
		case SDL_CONTROLLER_AXIS_RIGHTX:
			std::cout << "Right Stick X: " << evt.caxis.value << std::endl;
			break;
		case SDL_CONTROLLER_AXIS_RIGHTY:
			std::cout << "Right Stick Y: " << evt.caxis.value << std::endl;
			break;
		case SDL_CONTROLLER_AXIS_TRIGGERLEFT:
			std::cout << "Left Trigger: " << evt.caxis.value << std::endl;
			break;
		case SDL_CONTROLLER_AXIS_TRIGGERRIGHT:
			std::cout << "Right Trigger: " << evt.caxis.value << std::endl;
			break;
		}
	}


	void ControllerWrpr::OnButtonDown(SDL_Event evt) {
		switch(evt.cbutton.button) {
			case SDL_CONTROLLER_BUTTON_A:
				std::cout << "A pressed." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_B:
				std::cout << "B pressed." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_X:
				std::cout << "X pressed." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_Y:
				std::cout << "Y pressed." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_BACK:
				std::cout << "Back pressed." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_GUIDE:
				std::cout << "Guide pressed." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_START:
				std::cout << "Start pressed." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_LEFTSTICK:
				std::cout << "Leftstick Clicked." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_RIGHTSTICK:
				std::cout << "Rightstick Clicked." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_LEFTSHOULDER:
				std::cout << "L1/LB pressed." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_RIGHTSHOULDER:
				std::cout << "R1/RB pressed." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_DPAD_LEFT:
				std::cout << "Left pressed." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_DPAD_RIGHT:
				std::cout << "Right pressed." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_DPAD_UP:
				std::cout << "Up pressed." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_DPAD_DOWN:
				std::cout << "Down pressed." << std::endl;
				break;

		}
	}

	void ControllerWrpr::OnButtonUp(SDL_Event evt) {
		switch(evt.cbutton.button) {
			case SDL_CONTROLLER_BUTTON_A:
				std::cout << "A released." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_B:
				std::cout << "B released." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_X:
				std::cout << "X released." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_Y:
				std::cout << "Y released." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_BACK:
				std::cout << "Back released." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_GUIDE:
				std::cout << "Guide released." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_START:
				std::cout << "Start released." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_LEFTSTICK:
				std::cout << "Leftstick unClicked." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_RIGHTSTICK:
				std::cout << "Rightstick unClicked." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_LEFTSHOULDER:
				std::cout << "L1/LB released." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_RIGHTSHOULDER:
				std::cout << "R1/RB released." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_DPAD_LEFT:
				std::cout << "Left released." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_DPAD_RIGHT:
				std::cout << "Right released." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_DPAD_UP:
				std::cout << "Up released." << std::endl;
				break;
			case SDL_CONTROLLER_BUTTON_DPAD_DOWN:
				std::cout << "Down released." << std::endl;
				break;
		}
	}
	}